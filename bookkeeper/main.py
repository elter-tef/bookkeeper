from PySide6.QtWidgets import QApplication
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree
import sys

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

DB_NAME = 'test.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    cat_repo = SQLiteRepository[Category](DB_NAME, Category)
    exp_repo = SQLiteRepository[Expense](DB_NAME, Expense)

    if not cat_repo.get_all():
        Category.create_from_tree(read_tree(cats), cat_repo)

    view = MainWindow()
    model = None

    window = ExpensePresenter(model, view, cat_repo, exp_repo)
    window.show()
    app.exec()
