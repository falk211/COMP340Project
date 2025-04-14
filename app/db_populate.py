import hashlib
import psycopg
from app.db_info import *



def insert_sample_questions():
    try:
        # Connect to the database
        connection = psycopg.connect(f"host=dbclass.rhodescs.org dbname=practice user=user={DBUSER} password={DBPASS}")
        cursor = connection.cursor()


       # Multiple choice questions
        mc_questions = [
            (
                "Which C operator can be used to access a variable's address?",
                "multiple_choice",
                "easy",
                "C Basics",
                True,
                "*",
                "address_of()",
                "@",
                "&",
                3
            ),
            (
                "What is the correct way to dynamically allocate memory for an integer in C?",
                "multiple_choice",
                "medium",
                "C Memory Management",
                True,
                "int ptr = malloc(sizeof(int));",
                "int *ptr = malloc(sizeof(int));",
                "int ptr = malloc(sizeof(int *));",
                "int *ptr = malloc();",
                2
            ),
            (
                "What will happen if you try to dereference a NULL pointer in C?",
                "multiple_choice",
                "medium",
                "C Basics",
                True,
                "The program will print NULL.",
                "The program will execute normally.",
                "The program will cause a segmentation fault.",
                "The pointer will be automatically assigned to a valid address.",
                3
            ),
            (
                "Which function is used to release dynamically allocated memory in C?",
                "multiple_choice",
                "easy",
                "C Memory Management",
                True,
                "delete()",
                "release()",
                "free()",
                "remove()",
                3
            ),
            (
                "What is the purpose of sizeof() in C?",
                "multiple_choice",
                "easy",
                "C Functions",
                True,
                "It returns the memory address of a variable.",
                "It determines the size of a data type or variable in bytes.",
                "It allocates memory for a variable.",
                "It determines the number of elements in an array.",
                2
            ),
            (
                "Which command is used to list files and directories in Linux?",
                "multiple_choice",
                "easy",
                "Linux",
                True,
                "ls",
                "list",
                "show",
                "display",
                1
            ),
            (
                "What does the pwd command do in Linux?",
                "multiple_choice",
                "easy",
                "Linux",
                True,
                "Prints the working directory",
                "Changes the working directory",
                "Lists all files in the directory",
                "Displays system password information",
                1
            ),
            (
                "Which command is used to change file permissions in Linux?",
                "multiple_choice",
                "medium",
                "Linux",
                True,
                "chmod",
                "chperm",
                "setperm",
                "chown",
                1
            ),
            (
                "Which Linux command is used to display the contents of a file?",
                "multiple_choice",
                "easy",
                "Linux",
                True,
                "ls",
                "cat",
                "rm",
                "mv",
                2
            ),
            (
                "What is the purpose of the man command in Linux?",
                "multiple_choice",
                "easy",
                "Linux",
                True,
                "It manages user accounts",
                "It updates system software",
                "It opens the system manual pages for commands",
                "It monitors system performance",
                3
            ),
            (
                "Which symbol is used to redirect the output of a command to a file, overwriting existing content?",
                "multiple_choice",
                "hard",
                "Linux",
                True,
                ">",
                ">>",
                "|",
                "&",
                1
            ),
            (
                "How do you access a member of a struct using a pointer?",
                "multiple_choice",
                "medium",
                "C Basics",
                True,
                "structPtr.member",
                "structPtr->member",
                "*structPtr.member",
                "structPtr:*member",
                2
            ),
            (
                "What is the purpose of typedef when used with structs?",
                "multiple_choice",
                "medium",
                "C Basics",
                True,
                "It allows defining a struct without a name.",
                "It creates a new data type name for the struct.",
                "It dynamically allocates memory for the struct.",
                "It prevents modifications to the struct.",
                2
            )
        ]

        free_response = [
            (
                "Why do you have to prefix the program name with “./” when you want to execute it from a Linux/Unix shell?",
                "free_response",  # Changed from "multiple_choice"
                "easy",
                "Linux",
                True,
                "On Unix-style operating systems, programs are executed by specifying an absolute or relative path to their location or if the directory they reside is liked in the PATH environment variable."
            ),
            (
                "Which section of program memory stores the values of initialized global variables?",
                "free_response",  # Changed from "multiple_choice"
                "easy",
                "C Memory Basics",
                True,
                "It is stored in data."
            ),
            (
                "What value is typically stored in the first element of argv (i.e., argv[0])?",
                "free_response",  # Changed from "multiple_choice"
                "medium",
                "C Basics",
                True,
                "The program’s name or a relative/absolute executable path to that binary executable"
            )

        ]


        code_blocks = [
            (
                "Please complete this code",
                'code_blocks',
                'easy',
                'Programming',
                True,
                'this',
                'is',
                'a',
                'test',
                'code',
                'blocks',
                'of',
                'does it work?',
                '-1000',
                '-1000',
                '1,2,3,4,8,5,6,7,8',

            )
        ]

        # True/false questions
        tf_questions = [
            (
                "Does the size of a pointer depend on the type of the variable it points to?",
                "true_false",  # Changed from "true_false"
                "easy",
                "C Basics",
                True,
                False
            ),
            (
                "Is the size of an int always 4 bytes in C?",
                "true_false",  # Changed from "true_false"
                "easy",
                "C Basics",
                True,
                False
            ),
            (
            "Does the fgets() function in C stops reading input when it encounters a newline character?",
            "true_false",  # Changed from "true_false"
            "medium",
            "C Functions",
            True,
            True
            ),
            (
                "Do all C programs require a main() function?",
                "true_false",  # Changed from "true_false"
                "easy",
                "C Basics",
                True,
                True
            ),
            (
                "Can an array name be used as a pointer to its first element in C?",
                "true_false",  # Changed from "true_false"
                "medium",
                "C Basics",
                True,
                True
            ),
            (
                "Do functions use \"pass-by-refererence\" call semantics when calling whith arguments in C?",
                "true_false",  # Changed from "true_false"
                "medium",
                "C Basics",
                True,
                False
            ),
            (
                "Is a function prototype required every function before it is used in C?",
                "true_false",  # Changed from "true_false"
                "medium",
                "C Basics",
                True,
                False
            ),
            (
                "Is the dereference operator (*) used to access the value stored at a memory address in C?",
                "true_false",  # Changed from "true_false"
                "medium",
                "C Basics",
                True,
                True
            ),
            (
                "Will the OS automatically free memory allocated with malloc()?",
                "true_false",  # Changed from "true_false"
                "easy",
                "C Memory Management",
                True,
                False
            ),
            (
                "Does C support garbage collection like Java and Python?",
                "true_false",  # Changed from "true_false"
                "easy",
                "C Memory Management",
                True,
                False
            ),
            (
                "Can dereferencing a NULL pointer cause a segmentation fault?",
                "true_false",  # Changed from "true_false"
                "hard",
                "C Basics",
                True,
                True
            ),
            (
                "Can freeing a pointer twice (double free) cause a segmentation fault?",
                "true_false",  # Changed from "true_false"
                "hard",
                "C Basics",
                True,
                True
            )
        ]


        # Insert multiple choice questions
        for q in mc_questions:
            # Insert into questions table
            cursor.execute("""
                INSERT INTO questions (qtext, qtype, qlevel, qtopic, qactive)
                VALUES (%s, %s, %s, %s, %s) RETURNING qid
            """, (q[0], q[1], q[2], q[3], q[4]))

            qid = cursor.fetchone()[0]

            # Insert into multiple_choice table
            cursor.execute("""
                INSERT INTO multiple_choice (qid, option1, option2, option3, option4, answer)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (qid, q[5], q[6], q[7], q[8], q[9]))

        # Insert true/false questions
        for q in tf_questions:
            # Insert into questions table
            cursor.execute("""
                INSERT INTO questions (qtext, qtype, qlevel, qtopic, qactive)
                VALUES (%s, %s, %s, %s, %s) RETURNING qid
            """, (q[0], q[1], q[2], q[3], q[4]))

            qid = cursor.fetchone()[0]

            # Insert into true_false table
            cursor.execute("""
                INSERT INTO true_false (qid, correct)
                VALUES (%s, %s)
            """, (qid, q[5]))

        for q in free_response:
            # Insert into questions table
            cursor.execute("""
                INSERT INTO questions (qtext, qtype, qlevel, qtopic, qactive)
                VALUES (%s, %s, %s, %s, %s) RETURNING qid
            """, (q[0], q[1], q[2], q[3], q[4]))

            qid = cursor.fetchone()[0]

            # Insert into free_response table
            cursor.execute("""
                INSERT INTO free_response (qid, prof_answer)
                VALUES (%s, %s)
            """, (qid, q[5]))

        # Insert true/false questions
        for q in code_blocks:
            # Insert into questions table
            cursor.execute("""
                      INSERT INTO questions (qtext, qtype, qlevel, qtopic, qactive)
                      VALUES (%s, %s, %s, %s, %s) RETURNING qid
                  """, (q[0], q[1], q[2], q[3], q[4]))

            qid = cursor.fetchone()[0]

            # Insert into true_false table
            cursor.execute("""
                      INSERT INTO code_blocks (qid, block1, block2, block3, block4, block5, block6, block7, block8, block9, block10, answer)
                      VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)
                  """, (qid, q[5], q[6], q[7], q[8], q[9], q[10], q[11], q[12], q[13], q[14], q[15]))

        # Commit the changes
        connection.commit()
        print("Successfully inserted sample questions!")

        # Commit the changes

        user_service = UserFuncs()
        uname1 = 'Will'
        upass1 = 'testing'
        uemail1 = '123@456.com'
        uadmin1 = 0
        hashed_password1 = hashlib.sha256(upass1.encode()).hexdigest()

        uname2 = 'Matt'
        upass2 = 'iliketheory'
        uemail2 = 'abc@cdf.com'
        uadmin2 = 1
        hashed_password2 = hashlib.sha256(upass2.encode()).hexdigest()

        user_service.add_user(uname1, hashed_password1, uemail1, uadmin1)
        user_service.add_user(uname2, hashed_password2, uemail2, uadmin2)

        connection.commit()

        print('successfully inserted data')


    except psycopg.Error as e:
        print(f"An error occurred: {e}")
        connection.rollback()

    finally:
        # Close the connection
        connection.close()

if __name__ == "__main__":
    insert_sample_questions()