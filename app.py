from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import argparse
import os
import sys
from typing import Dict, List, Optional, Tuple

load_dotenv()

DB_CONFIG_KEYS = {
    'host': ('PGHOST', 'localhost'),
    'port': ('PGPORT', '5432'),
    'dbname': ('PGDATABASE', 'postgres'),
    'user': ('PGUSER', 'postgres'),
    'password': ('PGPASSWORD', '')
}

def extract_db_credentials() -> Dict[str, str]:
    credentials = {}
    for param_key, (env_var, fallback_val) in DB_CONFIG_KEYS.items():
        retrieved_value = os.environ.get(env_var, fallback_val)
        credentials[param_key] = int(retrieved_value) if param_key == 'port' else retrieved_value
    return credentials


def establish_database_connection():
    connection_params = extract_db_credentials()
    try:
        db_connection = psycopg2.connect(**connection_params)
        return db_connection
    except psycopg2.Error as connection_error:
        print(f"Database connection error: {connection_error}", file=sys.stderr)
        sys.exit(1)


def format_student_record_output(student_record: Dict) -> str:
    identifier = student_record['student_id']
    given_name = student_record['first_name']
    surname = student_record['last_name']
    contact_email = student_record['email']
    registration_date = student_record['enrollment_date']
    
    return f"{identifier:>3} | {given_name} {surname} | {contact_email} | {registration_date}"


def retrieve_complete_student_roster() -> List[Dict]:
    query_statement = """
        SELECT student_id, first_name, last_name, email, enrollment_date 
        FROM students 
        ORDER BY student_id ASC;
    """
    
    db_conn = establish_database_connection()
    try:
        with db_conn.cursor(cursor_factory=RealDictCursor) as query_cursor:
            query_cursor.execute(query_statement)
            retrieved_records = query_cursor.fetchall()
            
            if len(retrieved_records) == 0:
                print("No students found.")
                return []
            
            for individual_record in retrieved_records:
                formatted_output = format_student_record_output(individual_record)
                print(formatted_output)
            
            return retrieved_records
    finally:
        db_conn.close()


def insert_new_student_record(given_name: str, family_name: str, 
                              email_address: str, registration_date: Optional[str] = None) -> int:
    insertion_statement = """
        INSERT INTO students (first_name, last_name, email, enrollment_date) 
        VALUES (%s, %s, %s, %s) 
        RETURNING student_id;
    """
    
    parameter_tuple = (given_name, family_name, email_address, registration_date)
    db_conn = establish_database_connection()
    
    try:
        with db_conn.cursor() as modification_cursor:
            modification_cursor.execute(insertion_statement, parameter_tuple)
            generated_id = modification_cursor.fetchone()[0]
            db_conn.commit()
            
            print(f"Inserted student_id={generated_id} for {given_name} {family_name}")
            return generated_id
    finally:
        db_conn.close()


def modify_student_email_address(identifier: int, updated_email: str) -> bool:
    update_statement = "UPDATE students SET email = %s WHERE student_id = %s;"
    parameter_values = (updated_email, identifier)
    
    db_conn = establish_database_connection()
    try:
        with db_conn.cursor() as modification_cursor:
            modification_cursor.execute(update_statement, parameter_values)
            affected_count = modification_cursor.rowcount
            db_conn.commit()
            
            if affected_count == 0:
                print(f"No student found with id={identifier}")
                return False
            else:
                print(f"Updated email for student_id={identifier} -> {updated_email}")
                return True
    finally:
        db_conn.close()


def remove_student_by_identifier(target_id: int) -> bool:
    deletion_statement = "DELETE FROM students WHERE student_id = %s;"
    
    db_conn = establish_database_connection()
    try:
        with db_conn.cursor() as modification_cursor:
            modification_cursor.execute(deletion_statement, (target_id,))
            removed_count = modification_cursor.rowcount
            db_conn.commit()
            
            if removed_count == 0:
                print(f"No student found with id={target_id}")
                return False
            else:
                print(f"Deleted student_id={target_id}")
                return True
    finally:
        db_conn.close()


def configure_argument_parser() -> argparse.ArgumentParser:
    primary_parser = argparse.ArgumentParser(
        description="PostgreSQL CRUD operations for students table",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subcommand_parsers = primary_parser.add_subparsers(
        dest="operation",
        required=True,
        help="Specify operation to perform"
    )
    
    subcommand_parsers.add_parser("get_all", help="List all students")
    
    create_parser = subcommand_parsers.add_parser("add", help="Add a student")
    create_parser.add_argument("--first", required=True, 
                              dest="given_name",
                              help="First name")
    create_parser.add_argument("--last", required=True,
                              dest="family_name", 
                              help="Last name")
    create_parser.add_argument("--email", required=True,
                              dest="email_addr",
                              help="Email (unique)")
    create_parser.add_argument("--date",
                              dest="enroll_date",
                              help="Enrollment date YYYY-MM-DD (optional)")
    
    update_parser = subcommand_parsers.add_parser("update_email", 
                                                  help="Update student email by id")
    update_parser.add_argument("--id", type=int, required=True,
                              dest="student_identifier",
                              help="student_id")
    update_parser.add_argument("--email", required=True,
                              dest="new_email_value",
                              help="New email")
    
    delete_parser = subcommand_parsers.add_parser("delete", 
                                                  help="Delete student by id")
    delete_parser.add_argument("--id", type=int, required=True,
                              dest="target_student_id",
                              help="student_id")
    
    return primary_parser


def execute_requested_operation(parsed_arguments):
    operation_name = parsed_arguments.operation
    
    if operation_name == "get_all":
        retrieve_complete_student_roster()
        
    elif operation_name == "add":
        insert_new_student_record(
            parsed_arguments.given_name,
            parsed_arguments.family_name,
            parsed_arguments.email_addr,
            parsed_arguments.enroll_date
        )
        retrieve_complete_student_roster()
        
    elif operation_name == "update_email":
        modify_student_email_address(
            parsed_arguments.student_identifier,
            parsed_arguments.new_email_value
        )
        retrieve_complete_student_roster()
        
    elif operation_name == "delete":
        remove_student_by_identifier(parsed_arguments.target_student_id)
        retrieve_complete_student_roster()


def application_entry_point():
    argument_parser = configure_argument_parser()
    parsed_args = argument_parser.parse_args()
    execute_requested_operation(parsed_args)


if __name__ == "__main__":
    application_entry_point()