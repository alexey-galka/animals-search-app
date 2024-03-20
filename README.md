# Project Name

## Description
This repository contains the backend API documentation for the Project Name project. The API provides endpoints for managing users, animals, shelters, and administrative tasks related to the project.

Users can sign up, sign in, and manage their profiles. They can also create, update, and delete records of lost and found animals. Additionally, users can search for lost animals using specific criteria.

Shelters have functionalities to create, update, and delete shelter profiles. They can also manage volunteers associated with their shelter and create records for animals found within the shelter.

Volunteers can assist shelters by being associated with them. They have limited permissions, primarily revolving around their association with shelters.

Administrators have access to administrative endpoints allowing them to perform tasks such as viewing all users, animals, shelters, volunteers, and animal owners.

## Authentication
To access the endpoints, authentication is required. Users need to sign up and sign in to obtain authentication tokens.

## Roles and Permissions

### Owner
Owners have full control over their own profile and animals. They can also perform administrative tasks such as creating, updating, and deleting shelters.

### Shelter
Shelters have control over the animals in their shelter, including creating, updating, and deleting records of lost animals. They can also manage volunteers associated with their shelter.

### Volunteer
Volunteers can assist shelters by being associated with them. They have limited permissions, such as viewing shelter details and being added or removed from shelters.

## Endpoints

### Authentication

#### `/auth/sign-up` (POST)
Creates a new user.

#### `/auth/sign-in` (POST)
Logs in a user.

#### `/auth/logout` (POST)
Logs out a user.

#### `/auth/password-recovery` (POST)
Resets user password.

### Users

#### `/users/{user_id}` (GET)
Read user details.

### Animals

#### `/animals/create` (POST)
Creates a new record for a lost animal.

#### `/animals/{user_id}/all` (GET)
Reads all animals belonging to a user.

#### `/animals/{user_id}/lost` (GET)
Reads all lost animals belonging to a user.

#### `/animals/{user_id}/found` (GET)
Reads all found animals belonging to a user.

#### `/animals/{user_id}/{animal_id}` (GET)
Reads details of a specific lost animal.

#### `/animals/{user_id}/{animal_id}` (PUT)
Edits details of a specific lost animal.

#### `/animals/{user_id}/{animal_id}` (DELETE)
Deletes a specific lost animal.

#### `/search` (POST)
Searches for lost animals.

### Shelters

#### `/shelters/create` (POST)
Creates a new shelter.

#### `/shelters/{shelter_id}` (GET)
Reads details of a shelter.

#### `/shelters/{shelter_id}` (PUT)
Updates details of a shelter.

#### `/shelters/{shelter_id}` (DELETE)
Deletes a shelter.

#### `/shelters/{shelter_id}/volunteers` (GET)
Reads volunteers of a shelter.

#### `/shelters/{shelter_id}/volunteers/{volunteer_id}` (POST)
Adds a volunteer to a shelter.

#### `/shelters/{shelter_id}/volunteers/{volunteer_id}` (PUT)
Removes a volunteer from a shelter.

#### `/shelters/{shelter_id}/animals` (POST)
Creates a lost animal record for a shelter.

#### `/shelters/{shelter_id}/animals/edit/{animal_id}` (PUT)
Edits a lost animal record belonging to a shelter.

#### `/shelters/{shelter_id}/animals/{animal_id}` (DELETE)
Deletes a lost animal record belonging to a shelter.

#### `/shelters/{shelter_id}/animals/all` (GET)
Reads all animals belonging to a shelter.

#### `/shelters/{shelter_id}/animals/lost` (GET)
Reads all lost animals belonging to a shelter.

#### `/shelters/{shelter_id}/animalsfound` (GET)
Reads all found animals belonging to a shelter.

### Settings

#### `/settings/{user_id}/security/password-reset` (PUT)
Changes user password.

#### `/settings/main/{user_id}` (PUT)
Updates user profile.

#### `/settings/main/{user_id}` (DELETE)
Deletes user profile.

#### `/settings/main/{user_id}/avatar` (POST)
Updates user avatar.

### Admin

#### `/admin/users` (GET)
Reads all users.

#### `/admin/animals` (GET)
Reads all animals.

#### `/admin/shelters` (GET)
Reads all shelters.

#### `/admin/volunteers` (GET)
Reads all volunteers.

#### `/admin/owners` (GET)
Reads all animal owners.