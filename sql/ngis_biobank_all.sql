-- ngis_biobank_all
select extract(month from now()) as "FINANCIAL_MONTH",
	   extract(year from now()) as "FINANCIAL_YEAR",
	   now() as "DATE_AND_TIME_DATA_SET_CREATED",
	   '13R' as "ORGANISATION_IDENTIFIER_(CODE_OF_COMMISSIONER)",
	   '' as "ORGANISATION_IDENTIFIER_(CODE_OF_HISTOPATHOLOGY_LABORATORY_ENTITY)",
	   '' as "WITHHELD_IDENTITY_REASON",
	   patient_nhs_number as "NHS_NUMBER",
	   patient_ngis_id as "LOCAL_PATIENT_IDENTIFIER_(EXTENDED)",
	   patient_dob as "PERSON_BIRTH_DATE",
	   age(primary_sample_received_date, patient_dob) as "AGE_AT_ACTIVITY_DATE_(CONTRACT_MONITORING)",
	   '' as "DECEASED_INDICATOR ",
	   referral_id as "SHARED_REFERRAL_IDENTIFIER",
	   referral_id as "NGIS_REFERRAL_IDENTIFIER",
	   dispatched_sample_lsid as "SAMPLE_IDENTIFIER",
	   biobank_illumina_gel1001.clinical_indication_test_type_id AS "TEST_IDENTIFIER_OR_TEST_CODE",
	   well_id as "SAMPLE_WELL_IDENTIFIER",
	   '21' as "COMMISSIONED_SERVICE_CATEGORY_CODE",
	   'NCBPS20Z' as "SERVICE_CODE",
	   'TEST' as "POINT_OF_DELIVERY_CODE",
 	   biobank_illumina_gel1001.primary_sample_received_date as "SAMPLE_RECEIPT_DATE",
 	   '' as "PRELIMINARY_REPORT_ISSUE_DATE",
 	   '' as "PROVIDER_REFERENCE_NUMBER",
 	   '' as "NHS_SERVICE_AGREEMENT_LINE_NUMBER",
 	   '11' as "TEST_METHOD_CODE",
 	   biobank_illumina_gel1001.primary_sample_type as "SAMPLE_TYPE_CODE",
	   '' as "SAMPLE_PLATING_QUALITY_CONTROL",
	   '' as "SAMPLE_PLATING_QUALITY_CONTROL_FAIL_CODE",
	   dispatched_sample_volume_ul as "SAMPLE_VOLUME",
	   glh_concentration_ng_ul as "DNA_CONCENTRATION",
	   dispatched_sample_volume_ul*glh_concentration_ng_ul as "DNA_QUANTIFICATION",	    
	   '1' as "ACTIVITY_COUNT_(POINT_OF_DELIVERY)",
	   '' as "ACTIVITY_UNIT_PRICE",
	   '' as "TOTAL_COST",
	   biobank_illumina_gel1001.ordering_entity_id as "ORGANISATION_IDENTIFIER_(CODE_OF_ORDERING_ENTITY)"
from biobank_illumina_gel1001 
left join biobank_illumina_gel1005 on biobank_illumina_gel1001.dispatched_sample_lsid = biobank_illumina_gel1005.gel1001_id
left join biobank_illumina_gel1008 on biobank_illumina_gel1008.gel1001_id = biobank_illumina_gel1001.dispatched_sample_lsid
left join biobank_illumina_gel1010 on biobank_illumina_gel1010.laboratory_sample_id = biobank_illumina_gel1001.dispatched_sample_lsid




