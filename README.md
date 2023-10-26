# E-Commerce System

This is a comprehensive e-commerce system built with Django, integrating user authentication, shopping cart functionality, payment processing with Paystack, and user profiles.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- User Registration and Authentication.
- Product catalog and detail views.
- Shopping cart functionality.
- Checkout and payment processing using Paystack.
- User profile with the ability to update personal information.
- Responsive design for mobile and desktop.

## Requirements

- Python 3.x
- Django 3.x
- A Paystack account for payment processing.
- [Django crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) for form styling (used in the registration and profile forms).
- Additional Python libraries as specified in the project's `requirements.txt`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Levi-Chinecherem/e-commerce-system.git
   cd e-commerce-system
   ```
2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```
5. Create a superuser account to manage the admin panel:

   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:

   ```bash
   python manage.py runserver
   ```

The application will be accessible at `http://localhost:8000`.

## Usage

1. Visit the admin panel at `http://localhost:8000/admin/` and log in with your superuser account to manage products and users.
2. Browse the product catalog and add items to your cart.
3. Proceed to checkout, where you can complete your payment using Paystack.
4. Users can access their profiles to update personal information.

## Customization

To customize this e-commerce system, you can:

- Modify the HTML and CSS templates to match your branding.
- Add additional features such as product reviews or a blog.
- Enhance security and payment processing features.

## Documentation

For in-depth documentation on using and customizing this system, please refer to our [Wiki](https://github.com/yourusername/e-commerce-system/wiki).

## Contributing

We welcome contributions to improve this project. To contribute, please follow our [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code.

---

Happy e-commerce system building! 👩‍💻🛒
