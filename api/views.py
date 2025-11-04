# api/views.py

from django.contrib.auth.models import Group, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status

# Asegúrate de que estos Serializers estén definidos en api/serializers.py
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
)


# -------------------------------
# DECORADOR POR ROL
# -------------------------------
def role_required(role_name: str):
    """
    Úsalo sobre una vista: @role_required("Admin")
    Requiere autenticación y pertenencia al grupo indicado.
    """
    def decorator(view_func):
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response(
                    {"detail": "Authentication credentials were not provided."},
                    status=401
                )
            # Solo si el usuario es superuser o pertenece al rol
            if not request.user.is_superuser and not request.user.groups.filter(name=role_name).exists():
                return Response({"detail": f"Requiere rol: {role_name}"}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


# -------------------------------
# PERFIL / ROLES / PERMISOS
# -------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Devuelve el usuario autenticado con sus roles (grupos)."""
    return Response(UserSerializer(request.user).data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_permissions_view(request):
    """Lista todos los permisos efectivos del usuario autenticado."""
    perms = sorted(list(request.user.get_all_permissions()))
    return Response({"permissions": perms}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def roles_list_view(request):
    """Lista de roles disponibles (grupos)."""
    # Devolvemos roles como lista de objetos para que coincida con el JS de admin-roles.html
    roles = list(Group.objects.values('id', 'name')) 
    return Response(roles, status=200)


@api_view(["POST"])
@role_required("Admin")  # solo admin puede asignar roles
def assign_role_view(request):
    """
    Asigna un rol (grupo) a un usuario, buscando por email.
    Body (JSON): {"email": "usuario@ejemplo.com", "role": "Operador"}
    """
    email = request.data.get("email")
    role_name = request.data.get("role")

    if not email or not role_name:
        return Response({"detail": "email y role son requeridos"}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({"detail": "Usuario no existe"}, status=404)

    try:
        group = Group.objects.get(name=role_name)
    except Group.DoesNotExist:
        return Response({"detail": f"Rol '{role_name}' no existe"}, status=404)

    # Asigna el nuevo rol (limpiando los anteriores si solo debe tener uno)
    user.groups.clear()
    user.groups.add(group)
    return Response({"ok": True, "user": UserSerializer(user).data}, status=200)


# -------------------------------
# VISTAS: REGISTRO Y CAMBIO DE CONTRASEÑA
# -------------------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """Crea usuario nuevo y devuelve perfil, asignando el rol 'Operador' por defecto."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        DEFAULT_ROLE_NAME = "Operador" 
        try:
            default_group = Group.objects.get(name=DEFAULT_ROLE_NAME)
            user.groups.add(default_group)
        except Group.DoesNotExist:
            pass # No pasa nada si el rol no existe.
            
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """Permite al usuario autenticado cambiar su contraseña."""
    serializer = ChangePasswordSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Contraseña actualizada correctamente."}, status=200)
    return Response(serializer.errors, status=400)


# -------------------------------
# 🚨 VISTA UNIFICADA DE USUARIOS (CRUD) 🚨
# -------------------------------
@api_view(["GET", "DELETE"])
@role_required("Admin")
def users_list_view(request, pk=None):
    """
    Maneja GET (lista), DELETE (eliminación) de usuarios.
    PATCH (actualización de rol) se maneja a través de /roles/assign/
    """
    
    # Maneja la solicitud de Detalle/Acción (DELETE)
    if pk is not None:
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            # No se permite eliminar al propio usuario
            if user == request.user:
                return Response({"detail": "No puedes eliminar tu propia cuenta."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Si es GET con PK, devuelve el detalle del usuario (opcional)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    # Maneja la solicitud de Lista (GET)
    elif request.method == "GET":
        # Usamos filter(is_superuser=False) para no mostrar superusuarios en la lista de administración web
        users = User.objects.filter(is_superuser=False).order_by('email')
        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# -------------------------------
# EJEMPLO DE ENDPOINT PROTEGIDO POR ROL
# -------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@role_required("Admin")
def only_admin_example_view(request):
    return Response({"detail": "Hola Admin 👋"}, status=200)