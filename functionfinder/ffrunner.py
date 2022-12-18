# -*- coding: utf-8 -*-

# TODO: Run ff_runner as cli command w/ options (calc,clean,test)
# TODO: Run ff_runner as cli command w/ data as input argument \
#    (train, ideal, test)
# TODO: Conda oder PIP > in Variable speichern
# TODO: Verzeichnis venv anlegen, falls nicht vorhanden
# TODO: VE von file und aktivieren
# TODO: ggf Download von Git (Version checken?)

def main():
    """
    Run main module of the programm.

    Created on Wed Nov 30 00:34:26 2022

    @author: Grunsky
    """
    from .task import task
    task()
    #### VE laden
    # TODO: Overwrite VE am Ende des Programms für die nächste Benutzung
    print("# Load virtual environment")
    #    logging.debug("Load virtual environment")


# Only execute if script is called directly
# is this script called directly,
if __name__ == "__main__":
    # then execute the code above
    main()
