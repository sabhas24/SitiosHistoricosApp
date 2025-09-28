from src.models.database import db
from src.models.auth.user import user
from src.models.auth.role import Role
from src.models.auth.permission import Permission
from werkzeug.security import generate_password_hash, check_password_hash

def user_new(**kwargs):
    print(" 📝Creating a new user with the following details:")
    if 'password' in kwargs:
        kwargs['password'] = generate_password_hash(kwargs['password'])
    new= user(**kwargs)
    db.session.add(new)
    db.session.commit()
    print(f" ✅ User created with ID: {new.id}")
    return new
def user_check_password(email, password):
    user_obj=db.session.query(user).filter_by(email=email).first()
    if user_obj and check_password_hash(user_obj.password, password):
        print(f" ✅ Password for user '{email}' is correct.")
        return True
    print(f" ❌ Password for user '{email}' is incorrect or user does not exist.")
    return False
def user_index():
    return db.session.query(user).all()

def user_update(id, **kwargs):
    print(f" 📝Updating user with ID: {id}, {kwargs}")
    user = db.session.get(user, id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()
    print(f" ✅ User updated: {user}")
    return user
def user_detroy(id):
    print(f" 📝Deleting user with ID: {id}")
    user = db.session.get(user, id)
    if not user:
        print(f" ❌ User with ID {id} not found")
        return False
    db.session.delete(user)
    db.session.commit()
    print(f" ✅ User deleted")
    return True
def user_show(id):
    user = db.session.get(user, id)
    if not user:
        print(f" ❌ User with ID {id} not found")
        return None
    return user

def create_role(name):
    print(f" 📝Creating role: {name}")
    role = Role(name=name)
    db.session.add(role)
    db.session.commit()
    print(f" ✅ Role created with ID: {role.id} {role.name}")
    return role

def create_permission(name):
    print(f" 📝Creating permission: {name}")
    permission = Permission(name=name)
    db.session.add(permission)
    db.session.commit()
    print(f" ✅ Permission created with ID: {permission.id}")
    return permission

def assign_permission_to_role(role_name, perm_name):
    print(f" 📝Assigning permission '{perm_name}' to role '{role_name}'")
    role = db.session.query(Role).filter_by(name=role_name).first()  
    perm = db.session.query(Permission).filter_by(name=perm_name).first() 
    if role and perm and perm not in role.permissions:
        role.permissions.append(perm)
        db.session.commit()
        print(f" ✅ Permission '{perm_name}' assigned to role '{role_name}'")