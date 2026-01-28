# Bookshelf App Permissions and Groups

## Groups
1. Admins:
   - Permissions: can_view, can_create, can_edit, can_delete
   - Can perform all actions on books

2. Editors:
   - Permissions: can_create, can_edit
   - Can add and edit books but cannot delete

3. Viewers:
   - Permissions: can_view
   - Can only view books

## How it Works
- Permissions are defined in `Book` model under `Meta.permissions`.
- Users are assigned to groups via Admin or shell.
- Views enforce permissions using the `@permission_required` decorator.
  - Example: `@permission_required('bookshelf.can_edit', raise_exception=True)`
- Unauthorized access triggers a 403 Permission Denied.

## Adding New Permissions
1. Add a new entry in `Book.Meta.permissions`.
2. Run `python manage.py makemigrations` and `migrate`.
3. Assign the permission to relevant groups via Admin or shell.
