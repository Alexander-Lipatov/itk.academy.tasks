#   Создайте декоратор access_control, который ограничивает доступ 
# к функции на основе переданных ролей пользователя. Декоратор должен 
# принимать аргументы, определяющие допустимые роли (например, 
# @access_control(roles=['admin', 'moderator'])). Требования:

#   Если текущий пользователь имеет одну из допустимых ролей, 
# функция выполняется.
#   Если нет, выбрасывается исключение PermissionError с соответствующим 
# сообщением.
#   Реализуйте механизм определения текущей роли пользователя. Для целей 
# задания можно использовать глобальную переменную или контекстный менеджер.


from typing import Optional

def access_control(roles:Optional[list]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if user_role in roles:
                return func(*args, **kwargs)
            else:
                raise PermissionError("Access denied")
        return wrapper
    return decorator



@access_control(roles=['admin', 'moderator'])
def func():
    pass


user_role = 'admin'
func()


user_role = 'user'
func() 



