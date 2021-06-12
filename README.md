# Proposed Project: **KANBAN BOARD**

I am going to make a Kanban board website fitted for multiple unique users to create, edit, and accomplish tasks together. A kanban board is an organizational tool useful for projects between one or multiple people to manage what needs to be done. There are usually columns to represent work in various stages of the process like "To Do", "Doing", and "Complete". Individual tasks or jobs are written on cards and are moved across the columns to show progess and coordinate teams that are doing the work. 
A Kanban board tells everyone the status of a current project or job.
This method gives an easy view and optimized flow of work in progress that leaves room for continuous improvement.


## MVP Requirements
- Login user
- Create board
- Create Cards
- Drag and drop

## Fulfilling Project Requirements
- [x] This project will have users [log-in] and create a board. 
- [x]  The board owner can [create] the different stages of process for their project and create task cards that need to be done
- [x]  Users can expand view [read] boards and cards from the database
- [ ]  Users can be added to a card as the task "owner". There could be multiple users assigned to a card [Many-to-many]
- [x]  Users also have a profile page which can display details about them and which tasks they are assigned to [django-engine]
- [x]  User may [edit] profile or task data
- [x]  User may [delete] profile or tasks
- [ ]  People who are not logged in can see the kanban board but they cannot edit [protected]
- [x]  Application will have features like drag and drop and nice styling [static] content (CSS, images, JS)
- [x]  Tasks will have [validated] inputs to thoroughly explain the work at hand

## Bonus Stretch
- [ ]  May contain [file-uploads] for profile pictures
- [ ]  Cards may have checkboxes for jobs in a list that can only be moved after all checks are done.
- [x]  Drag and drop will [update] status of task card as you move it.