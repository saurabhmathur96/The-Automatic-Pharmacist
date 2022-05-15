symptom(headache).
symptom(sneezing).
symptom(runny_nose).
symptom(chills).
symptom(sore_throat).
symptom(fever). 
symptom(red_eyes).
symptom(watery_eyes).
symptom(nausea).
symptom(motion_sickness).
symptom(sleeplessness).
symptom(nausea).
symptom(diarrhea).
symptom(itchy_skin).
symptom(red_skin).
symptom(infected_skin).

ailment(common_cold).
ailment(flu).
ailment(conjunctivitis).
ailment(measles).
ailment(food_poisoning).
ailment(rash).

medicine(tylenol).
medicine(advil).
medicine(aspirin).
medicine(motrin).
medicine(nasalcrom).
medicine(flonase).
medicine(hydrocortisone).
medicine(zaditor).
medicine(benadryl).
medicine(dramamine).
medicine(bonine).


treats(tylenol, fever).
treats(advil, fever).
treats(motrin, fever).
treats(motrin, headache).
treats(advil, headache).
treats(flonase, rash).
treats(hydrocortisone, rash).
treats(zaditor, conjunctivitis).
treats(benadryl, sleeplessness).
treats(benadryl, cold).
treats(dramamine, nausea).
treats(dramamine, motion_sickness).
treats(bonine, motion_sickness).


factor(alcohol).
factor(tb_medication).
factor(pregnancy).
factor(high_bp_medication).
factor(blood_thinners).
factor(ace_inhibitors).
factor(lithium).

factor(tylenol).
factor(advil).
factor(aspirin).
factor(motrin).
factor(nasalcrom).
factor(flonase).
factor(hydrocortisone).
factor(zaditor).
factor(benadryl).
factor(dramamine).
factor(bonine).

% adverse_interaction(M, F) : medicine M has an adverse reaction with an existing factor F. F may be a drug or a condition.
adverse_interaction(tylenol, alcohol).
adverse_interaction(tylenol, tb_medication).

adverse_interaction(advil, alcohol).
adverse_interaction(advil, aspirin).
adverse_interaction(advil, pregnancy).
adverse_interaction(advil, high_bp_medication).

adverse_interaction(aspirin, alcohol).
adverse_interaction(aspirin, blood_thinners).
adverse_interaction(aspirin, advil).

adverse_interaction(motrin, ace_inhibitors).
adverse_interaction(motrin, lithium).
adverse_interaction(motrin, high_bp_medication).
adverse_interaction(motrin, pregnancy).

adverse_interaction(hydrocortisone, blood_thinners).
adverse_interaction(hydrocortisone, aspirin).


% has_ailment(P, A) : person P is diagnosed with ailment A
has_ailment(P, flu) :- person(P), has_symptom(P, fever), has_symptom(P, headache), has_symptom(P, chills), has_symptom(P, body_ache).
has_ailment(P, cold) :- person(P), has_symptom(P, headache), has_symptom(P, runny_nose), has_symptom(P, sneezing), has_symptom(P, sore_throat).
has_ailment(P, conjunctivitis) :- person(P), has_symptom(P, red_eyes), has_symptom(P, watery_eyes).
has_ailment(P, food_poisoning) :- person(P), has_symptom(P, bloating), has_symptom(P, nausea).
has_ailment(P, food_poisoning) :- person(P), has_symptom(P, diarrhea).
has_ailment(P, rash) :- person(P), has_symptom(P, itchy_skin), has_symptom(P, red_skin).
has_ailment(P, rash) :- person(P), has_symptom(P, infected_skin).

% can_take(P, M) : person P can take medicine M
can_take(P, M) :- person(P), medicine(M), not -can_take(P, M).
can_take(P, M) :- person(P), medicine(M), not -can_take(P, M).

% -can_take(P, M) : exception case - person P cannot take medicine M
-can_take(P, M) :- person(P), factor(X), existing(P, X), adverse_interaction(M, X).


% should_take(P, M) : person P should take medicine M to treat some symptom or some ailment
should_take(P, M) :- person(P), medicine(M), has_ailment(P, A), treats(M, A), can_take(P, M).
should_take(P, M) :- person(P), medicine(M), has_symptom(P, S), treats(M, S), can_take(P, M).

