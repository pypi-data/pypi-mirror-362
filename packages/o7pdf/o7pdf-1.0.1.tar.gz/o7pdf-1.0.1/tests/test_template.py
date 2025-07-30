import os
import shutil
import pytest
from o7pdf.template import Template


def test_basic():
    report = Template(
        filename="cache/template.pdf",
        title="O7 PDF Template",
        username="phil@o7conseils.com",
        updated="2021-09-01",
        orientation="landscape",
        # logo="logo.png",
    )
    report.add_page()

    report.report_head()

    report.section_title("Section 1")
    report.sub_title("Subsection 1.1")

    report.cell(
        text_trim=True,
        w=50,
        h=20,
        new_x="LEFT",
        new_y="NEXT",
        text=f"This is a great **Template**!",
        align="L",
        border=0,
        markdown=True,
    )
    report.cell(
        text_trim=True,
        w=50,
        h=20,
        new_x="LEFT",
        new_y="NEXT",
        text=f"This text needs to be trimmed to fit the cell width",
        align="L",
        border=1,
        markdown=True,
    )

    report.section_title("Section 2")
    report.sub_title("Subsection 2.1")

    report.save()


def test_deprecared_exception():
    report = Template(
        filename="cache/template.pdf",
        title="O7 PDF Template",
        username="phil@o7conseils.com",
        updated="2021-09-01",
        orientation="landscape",
        # logo="logo.png",
    )

    with pytest.raises(ValueError) as e_info:
        report.cell(
            text_trim=False,
            txt=f"This is a great **Template**!",
        )


def test_make_missing_dir():
    missing_dir = "cache/missing_dir"
    if os.path.exists(missing_dir):
        shutil.rmtree(missing_dir)

    report = Template(filename=f"{missing_dir}/template.pdf", title="O7 PDF Template").save()

    assert os.path.exists(missing_dir)
