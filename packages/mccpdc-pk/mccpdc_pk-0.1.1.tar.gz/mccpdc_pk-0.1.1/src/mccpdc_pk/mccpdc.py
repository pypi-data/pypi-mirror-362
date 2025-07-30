import polars as pl
from polars import col as c
import polars.selectors as cs

class MCCPDC:
    """
    MCCPDC provides static methods for loading, processing, and joining MCCPDC (Mark Cuban Cost Plus Drug Company) price data with other datasets using Polars.
    This class includes utilities to:
    - Load MCCPDC price data from a Parquet file.
    - Calculate differences in product sizes.
    - Compute incentive charges (IC) based on price and quantity.
    - Determine applicable MCCPDC fees depending on special handling.
    - Aggregate total MCCPDC charges.
    - Join MCCPDC price data to another dataset using as-of join logic.
    All methods are static and designed for use with Polars LazyFrames and Expressions.
    Methods:
        _load_mccpdc_price_file(mccpdc_path) -> pl.LazyFrame:
            Load MCCPDC data from a Parquet file as a LazyFrame.
        _size_diff() -> pl.Expr:
            Compute the absolute difference between 'size' and 'size_right' columns.
        _mccpdc_ic() -> pl.Expr:
            Calculate the MCCPDC Incentive Charge (IC) as price * quantity.
        _is_mccpdc_predicate() -> pl.Expr:
            Predicate to check if 'unit_price_w_markup' is not null.
        _mccpdc_fee(special_fee, standard_fee) -> pl.Expr:
            Compute the MCCPDC fee based on special handling status.
        _mccpdc_total(special_fee, standard_fee) -> list[pl.Expr]:
            Compute and return expressions for IC, fee, and total MCCPDC charge.
        add_mccpdc_price(data, mccpdc_file_path, special_fee, standard_fee) -> pl.LazyFrame:
            Join MCCPDC price data to the input dataset and add calculated columns.
    """

    @staticmethod
    def _load_mccpdc_price_file(mccpdc_path) -> pl.LazyFrame:
        """
        Load the MCCPDC data from a Parquet file.
        
        Returns:
            pl.DataFrame: The loaded MCCPDC data.
        """
        return pl.scan_parquet(mccpdc_path).with_columns(c.date.dt.month_end()).sort('date')

    @staticmethod
    def _size_diff() -> pl.Expr:
        """
        Calculate the absolute difference between the size and size_right columns.
        This is used to identify discrepancies in the size of products.
        """
        return (c.size - c.size_right).abs()
    
    @staticmethod
    def _mccpdc_ic() -> pl.Expr:
        """
        Calculate the MCCPDC IC (Incentive Charge) based on the price and quantity.
        This is done by multiplying the price (where the column name matches 'price.*mark')
        """
        return (cs.matches('(?i)price.*mark') * c.qty).round(2).alias('mccpdc_ic')

    @staticmethod
    def _is_mccpdc_predicate() -> pl.Expr:
        """
        Returns a Polars expression that checks if the 'unit_price_w_markup' column is not null.

        Returns:
            pl.Expr: A Polars expression evaluating to True where 'unit_price_w_markup' is not null.
        """
        return (c.unit_price_w_markup.is_not_null()) 
    
    @staticmethod
    def _mccpdc_fee(special_fee, standard_fee) -> pl.Expr:
        """
        Calculates the MCCPDC fee as a Polars expression based on special handling conditions.

        Args:
            special_fee: The fee to apply when special handling is required.
            standard_fee: The standard fee to apply when special handling is not required.

        Returns:
            pl.Expr: A Polars expression that evaluates to the special fee if both the MCCPDC predicate and special handling are true,
                    to the standard fee if only the MCCPDC predicate is true, or None otherwise.
        """
        # when the special_handling is True, return the special fee, otherwise return the standard fee
        special_handling_predicate = ((MCCPDC._is_mccpdc_predicate()) & (c.special_handling))
        return (
            pl.when(special_handling_predicate)
            .then(special_fee)
            .when(MCCPDC._is_mccpdc_predicate())
            .then(standard_fee)
            .otherwise(None).alias('mccpdc_fee')
        )


    @staticmethod
    def _mccpdc_total(special_fee, standard_fee) -> list[pl.Expr]:
        """
        Calculates and returns a list of Polars expressions related to MCCPDC totals.

        Args:
            special_fee: The special fee value to be used in the fee calculation.
            standard_fee: The standard fee value to be used in the fee calculation.

        Returns:
            list[pl.Expr]: A list containing:
                - The MCCPDC IC expression.
                - The MCCPDC fee expression (computed with special_fee and standard_fee).
                - The total MCCPDC expression (sum of IC and fee, rounded to 2 decimals, aliased as 'mccpdc_total').
        """
        
        mccpdc_total =  (MCCPDC._mccpdc_ic() + MCCPDC._mccpdc_fee(special_fee, standard_fee)).round(2).alias('mccpdc_total')
        return [
            MCCPDC._mccpdc_ic(),
            MCCPDC._mccpdc_fee(special_fee, standard_fee),
            mccpdc_total
        ]

    @staticmethod
    def add_mccpdc_price(data: pl.LazyFrame, mccpdc_file_path, special_fee, standard_fee, **kwargs) -> pl.LazyFrame:
        """
        Adds MCCPDC price information to the provided data by performing an as-of join with the MCCPDC price file.
        Parameters:
            data (pl.LazyFrame): The input data containing at least 'gpi', 'size', and 'is_brand' columns.
            mccpdc_file_path (str): Path to the MCCPDC price file to be loaded and joined.
            special_fee (float): The special fee to be applied in the MCCPDC total calculation.
            standard_fee (float): The standard fee to be applied in the MCCPDC total calculation.
        Returns:
            pl.LazyFrame: The input data augmented with MCCPDC price information, including calculated total prices.
        Raises:
            ValueError: If the input data does not contain the required columns: 'gpi', 'size', and 'is_brand'.
        Notes:
            - Performs an as-of join on 'dos' (date of service) and MCCPDC 'date', grouped by 'gpi' and 'is_brand'.
            - Calculates and adds MCCPDC total price columns using the provided fees.
            - Drops intermediate columns and renames joined columns for clarity.
        """
        if not all(col in data.collect_schema().names() for col in ['gpi', 'size', 'is_brand']):
            raise ValueError("Data must contain 'gpi', 'size', and 'is_brand' columns to join with MCCPDC prices.")

        mccpdc = MCCPDC._load_mccpdc_price_file(mccpdc_file_path)
        joined_data = (
            data
            .with_row_index('data_idx', 1)
            .sort(by='dos')
            .join_asof(
                mccpdc,
                left_on='dos',
                right_on='date',
                by=['gpi', 'is_brand'],
                strategy='forward',
                **kwargs
            )
            .sort(by=[MCCPDC._size_diff(),'size'],nulls_last=True)
            .unique('data_idx', keep='first', )
            .rename({
                'ndc_right': 'ndc_mccpdc',
                'date': 'date_mccpdc',
            })
            .with_columns(MCCPDC._mccpdc_total(special_fee, standard_fee))
            .drop('size_right')    
        )
        return joined_data    
