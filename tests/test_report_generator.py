from types import SimpleNamespace
from analysis.report_generator import ReportGenerator

def test_report_without_key_does_not_call_api(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY',raising=False)
    assert 'GEMINI_API_KEY' in ReportGenerator().generate_daily_insight([{'title':'Analyst'}])

def test_report_uses_company_name_and_handles_empty_data(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY',raising=False)
    generator=ReportGenerator();calls=[]
    def generate_content(**kwargs):calls.append(kwargs);return SimpleNamespace(text='Summary')
    generator.client=SimpleNamespace(models=SimpleNamespace(generate_content=generate_content))
    assert 'No hay' in generator.generate_daily_insight([])
    assert generator.generate_daily_insight([{'title':'Analyst','company_name':'Demo Co','sector':'Data'}])=='Summary'
    assert 'Demo Co' in calls[0]['contents']

def test_report_failure_returns_actionable_message(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY',raising=False)
    generator=ReportGenerator()
    def fail(**kwargs):raise RuntimeError('fake credential must not appear')
    generator.client=SimpleNamespace(models=SimpleNamespace(generate_content=fail))
    result=generator.generate_daily_insight([{'title':'Analyst'}])
    assert 'Revisa' in result and 'fake credential' not in result
