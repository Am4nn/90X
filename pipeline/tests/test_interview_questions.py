"""Parsing systemdesign.io's index.

The site has no semantic markup, so these tests pin the two things that were
silently wrong once already: difficulty read from the whole page instead of
the row, and company names scraped out of the title cell.
"""

from pipeline.normalize.interview_questions import follow_ups, rows_by_slug

# The complexity filter lists every level before the table starts. Reading
# difficulty by matching words across the page picks these up first and
# shifts every answer by four.
INDEX = """
<div class="filter">Very Easy Easy Medium Hard Very Hard</div>
<table><tbody>
<tr>
  <td><div>9</div></td>
  <td><a href="/question/design-an-api-rate-limiter"><div>Design an API Rate Limiter</div></a></td>
  <td><span>Amazon</span><span>Atlassian</span><span>Uber</span><span>+</span><span>2</span></td>
  <td><div>Hard</div></td>
</tr>
<tr>
  <td><div>23</div></td>
  <td><a href="/question/design-a-job-scheduler"><div>Design a Job Scheduler</div></a></td>
  <td><span>Google</span><span>Doordash</span></td>
  <td><div>Easy</div></td>
</tr>
</tbody></table>
"""


def test_difficulty_comes_from_the_row_not_the_page():
    rows = rows_by_slug(INDEX)
    assert rows["design-an-api-rate-limiter"]["difficulty"] == "Hard"
    assert rows["design-a-job-scheduler"]["difficulty"] == "Easy"


def test_companies_come_from_their_own_cell():
    """Guessing which cell held companies pulled words out of the title."""
    rows = rows_by_slug(INDEX)
    assert rows["design-a-job-scheduler"]["companies"] == ["Google", "Doordash"]
    assert "Design" not in " ".join(rows["design-an-api-rate-limiter"]["companies"])


def test_the_unnamed_company_count_is_dropped():
    """"Amazon Atlassian Uber + 2" names three; the +2 is not a company."""
    assert rows_by_slug(INDEX)["design-an-api-rate-limiter"]["companies"] == ["Amazon", "Atlassian", "Uber"]


def test_follow_ups_are_read_after_the_marker():
    page = """
    <p>Recommended solutions from the web. Sign up here?</p>
    <p>Here are some details you should know about this question:</p>
    <ul><li>How will you do this on a single machine first?</li>
    <li>How do you scale it across multiple machines to handle more jobs?</li></ul>
    """
    found = follow_ups(page)
    assert found == [
        "How will you do this on a single machine first?",
        "How do you scale it across multiple machines to handle more jobs?",
    ], found


def test_no_marker_means_no_follow_ups():
    assert follow_ups("<p>Nothing here.</p>") == []
