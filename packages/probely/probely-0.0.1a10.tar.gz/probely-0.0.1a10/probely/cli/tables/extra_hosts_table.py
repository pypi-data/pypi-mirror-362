from rich.table import Table
from probely.cli.tables.base_table import BaseOutputTable
from probely.sdk.models import ExtraHost


class ExtraHostTable(BaseOutputTable):
    @classmethod
    def create_table(cls, show_header: bool = False) -> Table:
        table = Table(show_header=show_header, box=None)

        table.add_column("ID", width=12)
        table.add_column("NAME", width=36, no_wrap=True)
        table.add_column("VERIFIED", width=8)
        table.add_column("HOST", width=48, no_wrap=True)
        table.add_column("INCLUDED", width=8)

        return table

    @classmethod
    def add_row(cls, table: Table, extra_host: ExtraHost) -> None:
        table.add_row(
            extra_host.id,
            extra_host.name,
            str(extra_host.verified),
            extra_host.host,
            str(extra_host.include),
        )
