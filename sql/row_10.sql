-- PLCM Query ROW 10 for Sample Plating
select referral_id as "NGIS_REFERRAL_IDENTIFIER",
	   dispatched_sample_lsid as "SAMPLE_IDENTIFIER",
	   biobank_illumina_gel1005.sample_received_datetime as "ACTIVITY_START_DATE_AND_TIME_(CONTRACT_MONITORING)",
	   biobank_illumina_gel1008.plate_date_of_dispatch as "ACTIVITY_END_DATE_AND_TIME_(CONTRACT_MONITORING)",
	   biobank_illumina_gel1008.plate_date_of_dispatch - biobank_illumina_gel1005.sample_received_datetime as "TURNAROUND_TIME_(CALENDAR_DAYS)",
   	   case 
	       when disease_area = 'Rare Disease' then '1'
	       when disease_area = 'Cancer' then '1'
       end as "TURNAROUND_TIME_STANDARD_(CALENDAR_DAYS)",
 	   'X' as "COMPLIANT_WITH_TURNAROUND_TIME_STANDARD",
   	   '8J834' as "ORGANISATION_IDENTIFIER_(CODE_OF_SUBMITTING_ORGANISATION)",
	   'T1460' as "ORGANISATION_IDENTIFIER_(CODE_OF_COMMISSIONED_ORGANISATION)",
	   'T1460' as "ORGANISATION_IDENTIFIER_(CODE_OF_SERVICE_PROVIDER)",
  	   'T1460' as "ORGANISATION_SITE_IDENTIFIER_(OF_SERVICE)",
   	   'TESTPLATE' as "LOCAL_POINT_OF_DELIVERY_CODE"
from biobank_illumina_gel1001 
left join biobank_illumina_gel1005 on biobank_illumina_gel1001.dispatched_sample_lsid = biobank_illumina_gel1005.gel1001_id
left join biobank_illumina_gel1008 on biobank_illumina_gel1008.gel1001_id = biobank_illumina_gel1001.dispatched_sample_lsid
left join biobank_illumina_gel1010 on biobank_illumina_gel1010.laboratory_sample_id = biobank_illumina_gel1001.dispatched_sample_lsid