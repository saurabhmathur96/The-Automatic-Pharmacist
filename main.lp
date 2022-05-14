can_take(P, M) :- person(P), medicine(M), not -can_take(P, M).
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

ailment(common_cold).
ailment(flu).
ailment(conjunctivitis).
ailment(measles).
ailment(diarrhea).
ailment(rash).

has_ailment(P, flu) :- person(P), has_symptom(P, fever), has_symptom(P, headache), has_symptom(P, chills), has_symptom(P, body_ache).
has_ailment(P, cold) :- person(P), has_symptom(P, headache), has_symptom(P, runny_nose), has_symptom(P, sneezing), has_symptom(P, sore_throat).

medicine(tylenol).
medicine(advil).
medicine(motrin).
medicine(nasalcrom).
medicine(flonase).

treats(tylenol, fever).
treats(motrin, headache).
treats(advil, headache).
treats(motrin, fever).
treats(flonase, rash).


can_take(P, M) :- person(P), medicine(M), not -can_take(P, M).
should_take(P, M) :- person(P), medicine(M), has_ailment(P, A), treats(M, A), can_take(P, M).
should_take(P, M) :- person(P), medicine(M), has_symptom(P, S), treats(M, S), can_take(P, M).


person(alice).
medicine(sugar).
treats(sugar, _).
has_symptom(alice, fever).
can_take(alice, sugar).

?- should_take(alice, X).
