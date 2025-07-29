import jwt


# Make sense to delete this function due to unsecure way to get sub from token
def get_user_sub_from_token(auth_string, default=None):
    """Returns the sub of a user from auth token."""
    try:
        return jwt.decode(auth_string, verify=False).get('sub', default)
    except Exception as ex:
        return 'default'
