
-- SNP Check referring GLH
--ngis_snp_referring_glh
select distinct referral_id , ordering_entity ->> 'organisation_grouping_location_code' as ods 
from biobank_illumina_gel1001 big 
order by referral_id 
