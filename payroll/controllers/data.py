import in_place
import pandas

from payroll.exception import GeneralError


class Data:

    @classmethod
    def load_data(cls, input_file):
        try:
            dataframe = pandas.read_csv(input_file, sep='\t+', comment='#', engine='python')
        except FileNotFoundError:
            raise GeneralError(f"Unable to find file: {input_file}")
        except Exception as exc:
            raise GeneralError(f"Unknown exception occurred: {exc}")
        else:
            return dataframe.replace({'{null}': None})

    @classmethod
    def dump_data(cls, output_file, user):
        try:
            with in_place.InPlace(output_file) as out:
                for line in out:
                    if line.startswith(user.username):
                        stringify = [str(item) for item in user.values]
                        stringify.append('\n')
                        new_line = '\t\t'.join(stringify)
                        line = line.replace(line, new_line)
                    out.write(line)
        except FileNotFoundError:
            raise GeneralError(f"Unable to find file: {output_file}")
        except Exception as exc:
            raise GeneralError(f"Unknown exception occurred: {exc}")
