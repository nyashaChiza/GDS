


def get_site(user):
    """Returns the site associated with the user based on their role."""
    if user.role == "Operator":
        return user.operation_site
    elif user.role == "Manager":
        return user.managed_site
    return None