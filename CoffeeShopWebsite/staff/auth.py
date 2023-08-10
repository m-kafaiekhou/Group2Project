#
#
#
# def authenticate(phone_number=None, password=None, **kwargs):
#     UserModel =
#     username = phone_number
#
#     if username is None:
#         username = kwargs.get(cls.UserModel.USERNAME_FIELD)
#     if username is None or password is None:
#         return
#     try:
#         user = cls.UserModel._default_manager.get_by_natural_key(username)
#     except cls.UserModel.DoesNotExist:
#         # Run the default password hasher once to reduce the timing
#         # difference between an existing and a nonexistent user (#20760).
#         cls.UserModel().set_password(password)
#     else:
#         if user.check_password(password) and cls.user_can_authenticate(user):
#             return user