-- PLCM Query SB

select patient_human_readable_stored_id as "LOCAL_PATIENT_IDENTIFIER_(EXTENDED)",
       case
           when c.concept_display = 'Male' then 1
           when c.concept_display = 'Female' then 2
           else 9
       end as "PERSON_STATED_GENDER_CODE",
       c2.concept_display as "ETHNIC_CATEGORY",
       address_postcode as "POSTCODE_OF_USUAL_ADDRESS",
	   r.referral_created_at as "TEST_REQUEST_DATE"    
from patient p 
join concept c 
on p.administrative_gender_cid = c.uid
join concept c2 
on p.ethnicity_cid = c2.uid
join 
referral_participant rp 
on p.uid = rp.patient_uid 
join address a 
on p.address_uid = a.uid 
join referral r 
on rp.referral_uid = r.uid 


