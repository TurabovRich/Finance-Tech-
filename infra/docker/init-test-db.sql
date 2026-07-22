-- Runs once when the `db` container's data volume is first initialized.
-- Creates a separate database for the test suite so `pytest` never touches
-- (and never risks dropping/recreating tables in) local dev data.
CREATE DATABASE clarity_test;
