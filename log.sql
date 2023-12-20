-- Keep a log of any SQL queries you execute as you solve the mystery.

--get: 2021/7/28, Humphrey Street
.table --to see what data is offered
.schema crime_scene_reports --starting off with this table
SELECT * FROM crime_scene_reports LIMIT 10; --see what's inside this table
SELECT * FROM crime_scene_reports WHERE year = '2021' AND month = '7' AND day = '28' AND street = 'Humphrey Street'; -- see data that matches the time of theft
--get: theft happens at 10:15am at the bakery. Have 3 witnessess.
SELECT * FROM interviews Limit 3; -- see this table
SELECT * FROM interviews WHERE year = '2021' AND month = '7' AND day = '28'; --select data that matches the time of theft
--get: Ruth(161): theif left with car at 10:15-10:25
--get: Eugene(162): theif at ATM, withdraw $, on Leggett Street that morning
--get: Raymond(163): accomplice talk to thief < 1min. earliest flight on 7/29 leaving fiftyville.


SELECT * FROM bakery_security_logs WHERE year ='2021' AND month = '7' AND day = '28' AND hour = '10' AND minute >= 15 AND minute <= 25; -- check Ruth's words
--THIEF: suspicious license plates
SELECT * FROM atm_transactions WHERE year = '2021' AND month = '7' AND day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'; -- check Eugene's words
--T: suspicious accounts
SELECT * FROM phone_calls WHERE year ='2021' AND month = '7' AND day = '28' AND duration < 60; --check Raymond's words on phonecalls
--A&T: suspicious phone numbers

SELECT * FROM flights WHERE year = '2021' AND month = '7' AND day = '29'; --check Raymond's words on flights.
SELECT * FROM airports WHERE city = 'Fiftyville'; --check airport id
SELECT * FROM airports WHERE id = 4;--check destination airport id
SELECT name, people.passport_number FROM passengers JOIN flights ON passengers.flight_id = flights.id JOIN people ON passengers.passport_number = people.passport_number WHERE flight_id = '36';
--T: suspicious passport num
--A&T: flight id = 36, 7/29 8:20 to LaGuardia Airport(NYC) -> ESCAPED TO NYC!!!

--goal: find thief w/ account, phone num, flight, license plate
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = '2021' AND month = '7' AND day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw');
--get: names of people with sus account
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = '2021' AND month = '7' AND day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw') AND phone_number IN (SELECT caller FROM phone_calls WHERE year ='2021' AND month = '7' AND day = '28' AND duration < 60);
--get: names of people with sus account and phone num
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = '2021' AND month = '7' AND day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw') AND phone_number IN (SELECT caller FROM phone_calls WHERE year ='2021' AND month = '7' AND day = '28' AND duration < 60) AND passport_number IN (SELECT people.passport_number FROM passengers JOIN flights ON passengers.flight_id = flights.id JOIN people ON passengers.passport_number = people.passport_number WHERE flight_id = '36');
--get: names of people with sus account, phone num, passport num
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = '2021' AND month = '7' AND day = '28' AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw') AND phone_number IN (SELECT caller FROM phone_calls WHERE year ='2021' AND month = '7' AND day = '28' AND duration < 60) AND passport_number IN (SELECT people.passport_number FROM passengers JOIN flights ON passengers.flight_id = flights.id JOIN people ON passengers.passport_number = people.passport_number WHERE flight_id = '36') AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year ='2021' AND month = '7' AND day = '28' AND hour = '10' AND minute >= 15 AND minute <= 25);
--get: names of people with sus account, phone num, passport num, license plate -> THIEF IS BRUCE!!!

--goal: find accomplice with phone num
SELECT phone_number FROM people WHERE name = 'Bruce';
--get: Bruce's phone num
SELECT receiver FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE name = 'Bruce') AND year ='2021' AND month = '7' AND day = '28' AND duration < 60;
--get: number who Bruce called
SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE name = 'Bruce') AND year ='2021' AND month = '7' AND day = '28' AND duration < 60);
--get: ACCOMPLICE IS ROBIN!!!