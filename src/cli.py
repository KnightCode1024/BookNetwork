import asyncio
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from core.database import async_session_maker
from services.user_service import UserService
from repositories.user_repository import UserRepository
from models.user import MyUserRole

app = typer.Typer(
    name="booklib-cli", help="Pereplet Management CLI", rich_markup_mode="rich"
)

console = Console()


@app.command()
def createsuperuser(
    username: Optional[str] = typer.Option(None, help="Логин администратора"),
    email: Optional[str] = typer.Option(None, help="Email администратора"),
    password: Optional[str] = typer.Option(None, help="Пароль администратора"),
):
    """
    [bold green]Создать суперпользователя[/bold green] 👑

    Создает пользователя с ролью администратора для доступа к админке.
    """

    async def _create_superuser():
        async with async_session_maker() as session:
            user_service = UserService(session)

            if not username:
                username_input = Prompt.ask("💻 [bold]Введите логин[/bold]")
            else:
                username_input = username

            if not email:
                email_input = Prompt.ask("📧 [bold]Введите email[/bold]")
            else:
                email_input = email

            if not password:
                password_input = Prompt.ask(
                    "🔑 [bold]Введите пароль[/bold]", password=True
                )
                confirm_password = Prompt.ask(
                    "🔑 [bold]Подтвердите пароль[/bold]", password=True
                )

                if password_input != confirm_password:
                    rprint("❌ [red]Пароли не совпадают![/red]")
                    return False
            else:
                password_input = password

            user_data = {
                "username": username_input,
                "email": email_input,
                "password": password_input,
                "is_active": True,
                "role": MyUserRole.ADMIN,
            }

            try:
                with console.status(
                    "[bold green]Создаю суперпользователя...[/bold green]"
                ):
                    admin_user = await user_service.create_user(user_data)

                rprint("✅ [bold green]Суперпользователь создан успешно![/bold green]")

                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Поле", style="dim")
                table.add_column("Значение")

                table.add_row("👤 Логин", admin_user.username)
                table.add_row("📧 Email", admin_user.email)
                table.add_row("👑 Роль", admin_user.role.value)
                table.add_row(
                    "✅ Статус", "Активен" if admin_user.is_active else "Неактивен"
                )

                console.print(table)
                return True

            except ValueError as e:
                rprint(f"❌ [red]Ошибка: {e}[/red]")
                return False
            except Exception as e:
                rprint(f"❌ [red]Неожиданная ошибка: {e}[/red]")
                return False

    success = asyncio.run(_create_superuser())
    raise typer.Exit(0 if success else 1)


@app.command()
def listusers():
    """
    [bold blue]Показать всех пользователей[/bold blue] 📋
    """

    async def _list_users():
        async with async_session_maker() as session:
            user_repo = UserRepository(session)

            with console.status("[bold blue]Загружаю пользователей...[/bold blue]"):
                users = await user_repo.get_all(limit=100)

            if not users:
                rprint("📭 [yellow]Пользователи не найдены[/yellow]")
                return

            table = Table(
                title="📋 Список пользователей",
                show_header=True,
                header_style="bold cyan",
            )

            table.add_column("ID", style="dim", width=6)
            table.add_column("Логин", width=20)
            table.add_column("Email", width=25)
            table.add_column("Роль", width=12)
            table.add_column("Активен", width=10)
            table.add_column("Создан", width=16)

            for user in users:
                status = "✅ Активен" if user.is_active else "❌ Неактивен"
                role_emoji = {"admin": "👑", "moderator": "🛡️", "user": "👤"}.get(
                    user.role, "❓"
                )

                table.add_row(
                    str(user.id),
                    user.username,
                    user.email,
                    f"{role_emoji} {user.role}",
                    status,
                    user.created_at.strftime("%d.%m.%Y %H:%M"),
                )

            console.print(table)
            rprint(f"📊 [dim]Всего пользователей: {len(users)}[/dim]")

    asyncio.run(_list_users())


@app.command()
def deactivate(username: str):
    """
    [bold yellow]Деактивировать пользователя[/bold yellow] ⚠️

    Аргументы:
        username: Логин пользователя для деактивации
    """

    async def _deactivate_user():
        async with async_session_maker() as session:
            user_repo = UserRepository(session)

            user = await user_repo.get_by_username(username)
            if not user:
                rprint(f"❌ [red]Пользователь '{username}' не найден[/red]")
                return False

            if not user.is_active:
                rprint(
                    f"ℹ️ [yellow]Пользователь '{username}' уже деактивирован[/yellow]"
                )
                return True

            if Confirm.ask(
                f"⚠️  Вы уверены, что хотите деактивировать пользователя [bold]{username}[/bold]?"
            ):
                user.is_active = False
                await session.commit()
                rprint(f"✅ [green]Пользователь '{username}' деактивирован[/green]")
                return True
            else:
                rprint("ℹ️ [yellow]Операция отменена[/yellow]")
                return False

    success = asyncio.run(_deactivate_user())
    raise typer.Exit(0 if success else 1)


@app.command()
def activate(username: str):
    """
    [bold green]Активировать пользователя[/bold green] ✅

    Аргументы:
        username: Логин пользователя для активации
    """

    async def _activate_user():
        async with async_session_maker() as session:
            user_repo = UserRepository(session)

            user = await user_repo.get_by_username(username)
            if not user:
                rprint(f"❌ [red]Пользователь '{username}' не найден[/red]")
                return False

            if user.is_active:
                rprint(f"ℹ️ [yellow]Пользователь '{username}' уже активен[/yellow]")
                return True

            user.is_active = True
            await session.commit()
            rprint(f"✅ [green]Пользователь '{username}' активирован[/green]")
            return True

    success = asyncio.run(_activate_user())
    raise typer.Exit(0 if success else 1)


@app.command()
def promote(username: str):
    """
    [bold purple]Назначить администратором[/bold purple] 👑

    Аргументы:
        username: Логин пользователя для повышения
    """

    async def _promote_user():
        async with async_session_maker() as session:
            user_repo = UserRepository(session)

            user = await user_repo.get_by_username(username)
            if not user:
                rprint(f"❌ [red]Пользователь '{username}' не найден[/red]")
                return False

            if user.role == "admin":
                rprint(
                    f"ℹ️ [yellow]Пользователь '{username}' уже администратор[/yellow]"
                )
                return True

            if Confirm.ask(
                f"👑 Назначить пользователя [bold]{username}[/bold] администратором?"
            ):
                user.role = "admin"
                await session.commit()
                rprint(
                    f"✅ [green]Пользователь '{username}' теперь администратор[/green]"
                )
                return True
            else:
                rprint("ℹ️ [yellow]Операция отменена[/yellow]")
                return False

    success = asyncio.run(_promote_user())
    raise typer.Exit(0 if success else 1)


@app.command()
def demote(username: str):
    """
    [bold orange]Снять права администратора[/bold orange] 📉

    Аргументы:
        username: Логин пользователя для понижения
    """

    async def _demote_user():
        async with async_session_maker() as session:
            user_repo = UserRepository(session)

            user = await user_repo.get_by_username(username)
            if not user:
                rprint(f"❌ [red]Пользователь '{username}' не найден[/red]")
                return False

            if user.role != "admin":
                rprint(
                    f"ℹ️ [yellow]Пользователь '{username}' не является администратором[/yellow]"
                )
                return True

            if Confirm.ask(
                f"📉 Снять права администратора у пользователя [bold]{username}[/bold]?"
            ):
                user.role = "user"
                await session.commit()
                rprint(
                    f"✅ [green]Пользователь '{username}' больше не администратор[/green]"
                )
                return True
            else:
                rprint("ℹ️ [yellow]Операция отменена[/yellow]")
                return False

    success = asyncio.run(_demote_user())
    raise typer.Exit(0 if success else 1)


@app.command()
def userinfo(username: str):
    """
    [bold cyan]Информация о пользователе[/bold cyan] 🔍

    Аргументы:
        username: Логин пользователя
    """

    async def _get_user_info():
        async with async_session_maker() as session:
            user_repo = UserRepository(session)

            user = await user_repo.get_by_username(username)
            if not user:
                rprint(f"❌ [red]Пользователь '{username}' не найден[/red]")
                return False

            table = Table(
                title=f"🔍 Информация о пользователе: {username}",
                show_header=True,
                header_style="bold cyan",
            )

            table.add_column("Поле", style="dim", width=15)
            table.add_column("Значение", width=30)

            role_emoji = {"admin": "👑", "moderator": "🛡️", "user": "👤"}.get(
                user.role, "❓"
            )

            status_emoji = "✅" if user.is_active else "❌"

            table.add_row("ID", str(user.id))
            table.add_row("Логин", user.username)
            table.add_row("Email", user.email)
            table.add_row("Роль", f"{role_emoji} {user.role}")
            table.add_row(
                "Статус",
                f"{status_emoji} {'Активен' if user.is_active else 'Неактивен'}",
            )
            table.add_row("Создан", user.created_at.strftime("%d.%m.%Y %H:%M"))
            table.add_row("Обновлен", user.updated_at.strftime("%d.%m.%Y %H:%M"))

            console.print(table)
            return True

    success = asyncio.run(_get_user_info())
    raise typer.Exit(0 if success else 1)


if __name__ == "__main__":
    app()
