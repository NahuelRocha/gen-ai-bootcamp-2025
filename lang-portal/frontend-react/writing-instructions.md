Development Instructions Writing Practice Component
1. Base Structure

Create a new component called WritingPractice
Implement routing for the /writing-practice path
Use shadcn/ui components to maintain visual consistency

2. User Flow
Implement the following flow:

User selects "Writing Practice" in the navigation
User selects a group of words to practice
System creates a new study session
System displays words one by one to practice
User types the translation and receives feedback
User can advance to the next word

3. Application States
Handle the following states:

Group selection
Active session
Current word
User input
Feedback status (correct/incorrect)
Practice progress

4. Data Handling

Store the ID of the active session
Maintain array of words from the selected group
Track current word index
Log correct/incorrect answers

5. Interactions

When selecting group:

Create new study session
Get words from group
Initialize practice status

When submitting response:

Validate translation
Record review in backend
Show feedback
Enable next word button

6. Visual Feedback

Display English word clearly
Input for Spanish translation
Visual indicator for correct/incorrect answer
Show correct translation after each attempt
Progress indicator in word group

7. Additional Considerations

Validations:

Input not empty
Active valid session
Selected group exists

Error handling:

Error in session creation
Error in word fetching
Error in review record

Accessibility:

Descriptive labels
Clear error messages
Keyboard navigation

Responsiveness:

Adaptive design for different screen sizes
Touch-friendly inputs for mobile devices

8. Testing Required

Functional group selection
Successful session creation
Correct response validation
Working review log
Smooth word navigation
Proper error handling

9. Success Criteria

User can select any available group
System creates sessions correctly
Immediate feedback on responses
Word statistics update
Smooth and error-free user experience
Design consistent with the rest of the application