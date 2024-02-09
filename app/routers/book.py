from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import List
import csv
import os

from app.schemas import User, Book
from app.oauth2 import get_current_user

router = APIRouter(tags=["Books"])


def csv_to_object_array(filename, key_names, ignore_header=True):
    """Reads a CSV file and converts it into an array of objects.

    Args:
        filename (str): The path to the CSV file.
        key_names (list): A list of strings representing the headers (keys) in the CSV file.
        ignore_header (bool, optional): Whether to skip the header row (default: True).

    Returns:
        list: An array of dictionaries representing the object structure for each row in the CSV file.
    """

    object_array = []
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile, key_names, restkey=None)

        if ignore_header:
            # Skip the header row if necessary
            next(reader, None)

        for row in reader:
            # Convert string values to appropriate data types
            for key, value in row.items():
                try:
                    row[key] = int(value)  # Attempt integer conversion first
                except ValueError:
                    try:
                        row[key] = float(value)  # Then try float conversion
                    except ValueError:
                        pass  # Leave as string if not convertible

            object_array.append(row)

    return object_array


# Function to read books from CSV file
def read_books_from_csv(file_name: str) -> List[str]:
    file_path = os.path.join("db", file_name)
    arr = csv_to_object_array(file_path, ["Book Name", "Author", "Publication Year"])
    print(arr)
    return arr


@router.get("/home")
def home(current_user: User = Depends(get_current_user)):
    if current_user.type == "admin":
        regular_books = read_books_from_csv("regularUser.csv")
        admin_books = read_books_from_csv("adminUser.csv")
        all_books = regular_books + admin_books
        return all_books
    elif current_user.type == "user":
        return read_books_from_csv("regularUser.csv")
    else:
        raise HTTPException(status_code=403, detail="Unauthorized user type")


# Function to add a book to CSV file
def add_book_to_csv(file_name: str, book_data: Book):
    file_path = os.path.join("db", file_name)
    with open(file_path, mode="a", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Book Name", "Author", "Publication Year"]
        )
        if file.tell() == 0:  # Check if file is empty
            writer.writeheader()
        book = {
            "Book Name": book_data.name,
            "Author": book_data.author,
            "Publication Year": book_data.publication_year,
        }
        writer.writerow(book)


# Define endpoint
@router.post("/addBook", status_code=201)
def add_book(
    book_data: Book = Body(...), current_user: str = Depends(get_current_user)
):
    if current_user.type != "admin":
        raise HTTPException(status_code=403, detail="Only admin users can add books")

    # Add book to CSV file
    add_book_to_csv("regularUser.csv", book_data)

    return {"message": "Book added successfully"}


# Function to delete a book from CSV file
def delete_book_from_csv(file_name: str, book_name: str):
    file_path = os.path.join("db", file_name)
    updated_records = []
    found = False
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Book Name"].lower() == book_name.lower():
                found = True
            else:
                updated_records.append(row)

    if not found:
        raise HTTPException(status_code=404, detail=f"Book '{book_name}' not found")

    with open(file_path, mode="w", newline="") as file:
        fieldnames = ["Book Name", "Author", "Publication Year"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_records)


# Define endpoint
@router.delete("/deleteBook", status_code=204)
def delete_book(
    book_name: str = Query(..., title="Book Name"),
    current_user: User = Depends(get_current_user),
):
    if current_user.type != "admin":
        raise HTTPException(status_code=403, detail="Only admin users can delete books")

    # Delete book from CSV file
    delete_book_from_csv("regularUser.csv", book_name)
