"""
FinanceFlow ETL Pipeline - Services Module

This module contains the main transaction processing service.
"""

from .transaction_processing_service import process_transaction_file

__all__ = ['process_transaction_file']
