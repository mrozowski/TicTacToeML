import view
import presenter
import ctypes


def main():

    myappid = u'mrozowski.tictactoe.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    """Creating MVP"""
    _view = view.View()
    _presenter = presenter.Presenter(_view)
    _view.set_presenter(_presenter)

    _presenter.show()



if __name__ == "__main__":
    main()