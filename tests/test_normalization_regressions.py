from etl.normalizers import DataNormalizer
from etl.enrichment import CompanyEnricher


def test_explicit_seniority_overrides_manager_title():
    normalizer = DataNormalizer()
    assert normalizer.normalize_seniority('Junior', 'Account Manager') == 'Junior'
    assert normalizer.normalize_seniority('Semi-senior', 'Developer') == 'Mid'
    assert normalizer.normalize_seniority(None, 'Product Manager') == 'Other'


def test_job_type_reads_description_even_when_title_is_present():
    assert DataNormalizer().normalize_job_type('Developer', 'Trabajo remoto') == 'Remote'


def test_unknown_company_does_not_invent_headquarters():
    info = CompanyEnricher().enrich_company_info('Nombre sin ubicación')
    assert info['hq_country'] == 'No especificado'
    assert info['inference_method'] == 'name_heuristic'
