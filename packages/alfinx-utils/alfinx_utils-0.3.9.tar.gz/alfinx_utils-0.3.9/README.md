alfinx_autho is a lightweight Python package designed to simplify authentication in FastAPI applications via HTTP headers. It automatically detects x-api-key and x-service-code headers from incoming requests and sends them, along with environment variables AUTHENTICATION_API_URL and X_SERVICE_ORIGIN_CODE, to an external authentication service for verification.

Installation

To install the package, run the following command:


pip install alfinx_utils

from alfinx import check_authentication,decrease_user_limit,save_data_on_mongo

Postman
Headers:

x-api-key: (sənin API açarın)
x-service-code: (sənin xidmət kodun)
