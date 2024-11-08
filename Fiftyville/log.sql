-- We have been told that the theft took place on July 28, 2023 and that it took place on Humphrey Street:
SELECT description
FROM crime_scene_reports
WHERE street = 'Humphrey Street'
    AND year = 2023
    AND month = 7
    AND day = 28

-- Going off the fact that it took place on Humphrey Street 7/28/2023,
-- We can check for any interviews conducted on that day to find potential
-- clues as to where the thief might have went or what he/she was doing
-- on that day according to eye witnesses.

SELECT transcript
FROM interviews
WHERE day = 28
    AND month = 7
    AND year = 2023;

-- Based off of the interviews conducted on that day, we can assume that:
-- The thief got into a car in the bakery parking lot and drove away.
-- The thief was spotted withdrawing money on Leggett Street
-- The thief called someone for less than a minute, in the call he was heard asking
-- someone to purchase the flight ticket for his/her escape
-- Based off of all this information, we can put together a very long query
-- using every piece of "evidence" or clues we have from these interviews.

SELECT *
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE activity = 'exit' AND year = 2023
    AND month = 7 AND day = 28
    AND hour = 10 AND minute BETWEEN 15 and 50
)
AND phone_number IN(
    SELECT caller
    FROM phone_calls
    WHERE day = 28 AND duration < 60
    AND year = 2023 AND month = 7
)
AND people.id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE bank_accounts.account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2023 AND month = 7
        AND day = 28 AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
        ORDER by amount
    )
);

-- The very long query above narrows our list down to just 3 suspects.
-- We can now assume that it's either Taylor, Diana or Bruce.
-- However, we'd like to reduce this list to just one person
-- so that we can accurately identify our thief.
-- We'll start off by acquiring the number of each of the 3,
-- and then continue on with our investigation.

SELECT *
FROM people
WHERE phone_number IN (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2023
    AND month = 7
    AND day = 28
    AND duration < 60
    AND caller IN ("(286) 555-6063", "(770) 555-1861", "(367) 555-5533")
);

-- With the query above, we get back 3 names.
-- James, Phillip and Robin. We can assume that one of the three
-- is an accomplice of whoever the thief is.
-- To get 3 pairs of suspects, we'll run the following query:

SELECT *
FROM phone_calls
WHERE year = 2023
    AND month = 7
    AND day = 28
    AND caller IN ("(286) 555-6063", "(770) 555-1861", "(367) 555-5533")
    AND receiver IN ("(676) 555-6554", "(725) 555-3243", "(375) 555-8161");

-- The query above tells us the following:
-- Bruce called Robin
-- Taylor called James
-- Diana called Philip.
-- We have now narrowed it down even further.
-- The thief was talking on the phone (7/28) about leaving Fiftyville "tomorrow" as early as possible.
-- From this we have a big clue and we're going to check flights departing the next day (7/29)

SELECT *
FROM flights
JOIN airports ON airports.id = flights.origin_airport_id
    WHERE flights.year = 2023
    AND flights.month = 7
    AND flights.day = 29
    AND airports.city = 'Fiftyville'
    ORDER by flights.hour, flights.minute;

-- With the query just above, we get back 5 flights.
-- Assuming that the thief left as early as possible, as said on the call,
-- it's safe to say that the two we should be looking at here are:
-- Fiftyville to New York at 08:20AM and Fiftyville to Chicago at 09:30AM

SELECT id, hour, minute FROM flights
    WHERE year = 2023
    AND month = 7
    AND day = 29
    AND origin_airport_id IN (
        SELECT id FROM airports
            WHERE city = "Fiftyville"
    )
    ORDER BY hour, minute;

-- The query above shows that the earliest flight
-- out of Fiftyville, on the 29th of the 7th, has the id 36.


SELECT passport_number FROM passengers
    WHERE flight_id = 36;

-- Using the id of the flight, we can
-- determine the passport_numbers
-- of every passenger on that flight with the query above.
-- With all of the above, we can move on because the information
-- we currently have will be sufficient for this next part.


SELECT name, phone_number FROM people
    WHERE id IN (
        SELECT person_id FROM bank_accounts
            WHERE account_number IN
                (SELECT account_number FROM atm_transactions
                    WHERE year = 2023
                    AND month = 7
                    AND day = 28
                    AND atm_location = "Leggett Street"
                    AND transaction_type = "withdraw")
                    )
    AND license_plate IN (
        SELECT license_plate FROM bakery_security_logs
            WHERE year = 2023
            AND month = 7
            AND day = 28
            AND hour = 10
            AND minute > 15
            AND minute <= 25
            )
    AND phone_number IN (
        SELECT caller FROM phone_calls
            WHERE year = 2023
            AND month = 7
            AND day = 28
            AND duration < 60
            )
    AND passport_number IN (
        SELECT passport_number FROM passengers
            WHERE flight_id = 36
            );


-- With this very long query, we are able to
-- narrow down our answer to just one: Bruce.
-- Let us now figure out who Bruce's accomplice is.
-- We can figure this out by checking who Bruce called.

SELECT receiver FROM phone_calls
    WHERE "(367) 555-5533" = caller
    AND year = 2023
    AND month = 7
    AND day = 28
    AND duration < 60;

-- Running this query gives us his accomplice's number.

SELECT name FROM people
    WHERE phone_number = "(375) 555-8161";

-- With this, we have the accomplice's name: Robin.


SELECT city FROM airports
    WHERE id =
        (SELECT destination_airport_id FROM flights
            WHERE id = 36);

-- By using the id of 36 (for the flight), we have
-- narrowed our search down to New York City or LaGuardia Airport.

-- This was CS50

