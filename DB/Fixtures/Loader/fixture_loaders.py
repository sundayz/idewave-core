import subprocess
from os import walk, path, listdir

from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from DB.Connection.WorldConnection import WorldConnection
from Utils.Debug.Logger import Logger

from Config.Run.config import Config

class FixtureLoader:
    def __init__(self):
        self._fixtures_directory = 'DB/Fixtures'

    def load_data(self) -> None:
        raise NotImplementedError

    def _get_fixtures(self, fixture_dir: str):
        """
        :param fixture_dir:
        :return: A list of paths to all the fixtures (e.g. /db/fixtures/01_data.sql)
        """
        fixtures_path = path.join(self._fixtures_directory, fixture_dir)
        files = [path.join(fixtures_path, f) for f in listdir(fixtures_path) if path.isfile(path.join(fixtures_path, f))]
        return files


class WorldFixtureLoader(FixtureLoader):
    def __init__(self):
        super().__init__()
        self._connection = WorldConnection()

    def load_data(self) -> None:
        files = self._get_fixtures('World')
        for file_name in files:
            try:
                with open(file_name, 'r') as file:
                    Logger.notify('Start loading {}'.format(file_name))
                    statement = file.read()
                    # self._connection.engine.execute(statement)
                    self._connection.session.execute(statement)
                    Logger.success('{} successfully imported'.format(file_name))
            except (DBAPIError, SQLAlchemyError) as ex:
                # SQLAlchemy exceptions print out the entire .sql files so we truncate the error message
                ex = str(ex)
                error_msg = ex if len(ex) < 255 else '{}... (truncated)'.format(ex[:255])
                Logger.error('Failed to load fixture {}\n{}'.format(file_name, error_msg))
                break
            except Exception as ex:
                Logger.error('Failed to load fixture {}\n\t{}'.format(file_name, ex))
                break
