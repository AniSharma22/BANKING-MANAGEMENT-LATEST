# Authentication & Authorization Errors (1000-1999)
INVALID_CREDENTIALS_ERROR = 1001      # Invalid username or password
USER_EXISTS_ERROR = 1002              # User with this email already exists
OPERATION_NOT_PERMITTED_ERROR = 1003   # User doesn't have permission for this operation
UNAUTHORIZED_ACCESS_ERROR = 1004       # User not authorized to access this resource

# Token Related Errors (1100-1199)
INVALID_TOKEN_PAYLOAD_ERROR = 1101     # Token payload is malformed or invalid
INVALID_TOKEN_ERROR = 1102             # Token is invalid
EXPIRED_TOKEN_ERROR = 1103             # Token has expired

# Validation Errors (2000-2999)
VALIDATION_ERROR = 2001                # General validation error
INVALID_UUID_ERROR = 2002              # UUID format is invalid
FIELD_MISSING_ERROR = 2003             # Required field is missing
INVALID_TRANSACTION_TYPE_ERROR = 2004   # Invalid transaction type specified

# Resource Not Found Errors (3000-3999)
ACCOUNT_NOT_EXISTS_ERROR = 3001        # Account doesn't exist
BANK_NOT_EXISTS_ERROR = 3002           # Bank doesn't exist
BRANCH_NOT_EXISTS_ERROR = 3003         # Branch doesn't exist

# Resource Already Exists Errors (4000-4999)
ACCOUNT_EXISTS_ERROR = 4001            # Account already exists

# System & Database Errors (5000-5999)
DATABASE_ERROR = 5001                  # Database operation failed
SYSTEM_ERROR = 5002                    # Internal system error
UNEXPECTED_ERROR = 5003                # Unexpected error occurred