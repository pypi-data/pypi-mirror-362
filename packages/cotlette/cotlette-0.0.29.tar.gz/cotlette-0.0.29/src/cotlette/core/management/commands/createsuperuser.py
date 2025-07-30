import getpass
import random
import string
from cotlette.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Creates a superuser account (a user with all permissions). "
        "This is equivalent to calling create_user() with is_superuser=True."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            help="Username for the superuser",
        )
        parser.add_argument(
            "--email",
            help="Email address for the superuser",
        )
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_true",
            help="Tells Cotlette to NOT prompt the user for input of any kind. "
            "You must use --username with --noinput, along with an option for "
            "any other required field. Superusers created with --noinput will "
            "not be able to log in until they're given a valid password.",
        )

    def handle(self, **options):
        username = options.get("username")
        email = options.get("email")
        noinput = options.get("noinput")

        # Try to get the User model
        try:
            from cotlette.core.database.models import ModelMeta
            UserModel = ModelMeta.get_model("UserModel")
            if not UserModel:
                # Try alternative model names
                UserModel = ModelMeta.get_model("User")
                if not UserModel:
                    raise CommandError(
                        "Could not find User model. Make sure you have a User model "
                        "defined in your apps (e.g., apps.users.models.UserModel)."
                    )
        except ImportError:
            raise CommandError(
                "Could not import User model. Make sure your apps are properly configured."
            )

        # Create the superuser
        if noinput:
            if not username:
                raise CommandError("You must use --username with --noinput.")
            if not email:
                raise CommandError("You must use --email with --noinput.")
            
            password = self._get_random_password()
            self.stdout.write(
                f"Superuser created successfully with password: {password}"
            )
        else:
            username = self._get_username(username)
            email = self._get_email(email)
            password = self._get_password()

        # Check if user already exists
        existing_user = UserModel.objects.filter(email=email).first()
        if existing_user:
            raise CommandError(f"User with email '{email}' already exists.")

        # Hash the password
        try:
            import bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        except ImportError:
            # Fallback to simple hash if bcrypt is not available
            import hashlib
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Create the superuser
        try:
            superuser = UserModel.objects.create(
                name=username,
                email=email,
                password_hash=hashed_password,
                # Add any other required fields with default values
                age=0,  # Default age
                organization="Admin",  # Default organization
                group=1,  # Default group ID (you might need to adjust this)
            )
            self.stdout.write(
                f"Superuser '{username}' created successfully."
            )
        except Exception as e:
            raise CommandError(f"Error creating superuser: {e}")

    def _get_username(self, username=None):
        """Get username from user input."""
        while not username:
            username = input("Username: ").strip()
            if not username:
                self.stdout.write("Username cannot be blank.")
        return username

    def _get_email(self, email=None):
        """Get email from user input."""
        while not email:
            email = input("Email address: ").strip()
            if not email:
                self.stdout.write("Email address cannot be blank.")
            elif "@" not in email:
                self.stdout.write("Enter a valid email address.")
                email = ""
        return email

    def _get_password(self):
        """Get password from user input."""
        while True:
            password = getpass.getpass("Password: ")
            if not password:
                self.stdout.write("Password cannot be blank.")
                continue
            
            password_confirm = getpass.getpass("Password (again): ")
            if password != password_confirm:
                self.stdout.write("Passwords don't match.")
                continue
            
            if len(password) < 8:
                self.stdout.write(
                    "Password is too short. It must contain at least 8 characters."
                )
                continue
            
            return password

    def _get_random_password(self):
        """Generate a random password for --noinput mode."""
        # Generate a random password
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(12))
        return password 