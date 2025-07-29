__version__ = "0.1.0"
__author__ = "CONTACT Software GmbH"
__email__ = "ptm-team@contact-software.com"

def hello():
    """A simple hello function for testing."""
    return "Hello from dummy test package!"

def main():
    """Main function that can be called from command line."""
    print(hello())

if __name__ == "__main__":
    main()
