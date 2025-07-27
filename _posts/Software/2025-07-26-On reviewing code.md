---
layout: post
tags:
  - Software
---
Working at a place that is dominantly online and not in office I've come to realise that a large proportion of the value we produce is not in the code you write but in the code you review as well.

If this is true, it makes a lot of sense to invest in the skill of reviewing code as much as I have already invested into the art of coding.

This post aims to tackle as a guide and cook book for performing better code reviews.

## What is the purpose of a code review?
A good way of thinking about a code review is as a process of adding value to existing code.

So how can you add value to existing code?
1. Make it more simpler
2. Make is more correct
3. Make it more performant

Another perspective is that the purpose of a code review is to fight against the natural nature of a codebases, they deteriorate in quality over time. Like a ratchet each time you loosen the bar, it stays there, and never goes back. The core principle being:

>  In general, reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn't perfect.

## What to figure out in a code review?

The functionality
- Does the code do what the developer intended
- Is what the developer intending necessary
- Are there any edge cases
- Are there any concurrency problems
- Are there any bugs
- Can it cause deadlocks or race conditions

The complexity
- Can it be simpler
- Is it too generic
- Is it solving additional problems

The tests
- Are there tests?
- Are there all the tests for edge cases
- Are the tests simple

The naming
- Do the names make sense?

The comments
- Are the comments necessary
- Are there comments explaining **why** some code exists, not how it works

The observability
- Can I detect that this code fail
- Is there any visibility loss?

The style
- Is it well indented?
- Is it consistent with the codebase?
- Do I want to maintain this?

The broader context
- Is the code improving the code health of the system or is it making the whole system more complex
- **Don't accept code that degrades the code health of the system, THEY ADD UP.**

The good things
- What are the good things, you like

In summary
- The code is well-designed.
- The functionality is good for the users of the code.
- Any parallel programming is done safely.
- The code isn't more complex than it needs to be.
- The developer isn't implementing things they might need in the future but don't know they need now.
- Code has appropriate unit tests.
- Tests are well-designed.
- The developer used clear names for everything.
- Comments are clear and useful, and mostly explain why instead of what.

## How do you actually do a code review

1. Does the intent make sense?
2. Look at the most important part of the change.
3. Look at the rest of the code.


**Does it make sense?**
- Does the description make sense
- Is it needed

**Look at the core logical impl**
- Try to find major design problems first, so you don't need to review the rest of the impl.
- Major changes take a while so you want to give feedback quickly

**Look at the rest**
- Review all the files, now with the context of whats happening

## On speed
The velocity of the team is dependant on iteration speed, so quick reviews are the life blood of the team. **You should do a code review shortly after it comes in!**

## On pitfalls
1. Don't have multiple round trips, reduce this time as much as possible
2. Don't make it a ransom note, don't hold the review hostage
3. Don't have two conflicting reviewers fighting with each other
4. Don't have a guessing game. Don't just criticise the solution and not give a solution. Make it specific. Not a vague hammer to hit them.
5. Start with the bombshell, not the nits. The nits come after the major design reworks.
6. Never flip slop between your thoughts.


## On comments

General idea is to do something like this
1. What is wrong with the code?
2. **Why** is it wrong?
3. How to fix it? **Be actionable!**

And to place color on
- Is it blocking?
- So they don't waste time on bikesheds!

Something to consider is labelling comment severity
1. Nit: This is minor
2. Optional: I think this may be a good idea
3. FYI: Could be interesting

Additional principles
- Never say the word **you** in a code review: never attack the author, say **WE**!
- Use the passive voice. **Only ask questions**, What about renaming this variable?
- You aren't commanding them, you're suggesting ideas to make this code better.
- Tie your feedback to principles.

## And finally on the other side, what should you consider as the author

A pretty fun graphic from cisco code reviews shows that at most 400 lines of code, the amount of issues you can notice significantly diminish. So try to split it up!


![](https://static1.smartbear.co/smartbear/media/images/product/collaborator/code-review-best-practices-figure-01.gif)


What makes a code review small?
- It does one thing
- It tests that one thing
- What are the implications of this one thing

So how can you split up a change?
- Stack changes, pull out precursors and incrementally contribute
- Split by files, update each file change independently
- Split horizontally: design your code in such a way that you can easily cut multiple code reviews without them interfering
- Split by intent/ logical change
- Split out refactors

## Appendix
<https://github.com/google/eng-practices/blob/master/review/index.md>

<https://www.chiark.greenend.org.uk/~sgtatham/quasiblog/code-review-antipatterns/>

<https://philbooth.me/blog/the-art-of-good-code-review>

<https://bitfieldconsulting.com/posts/code-review>

<https://lindbakk.com/blog/code-reviews-easy-in-theory-difficult-in-practice>

<https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/>

<https://mtlynch.io/human-code-reviews-1/#start-reviewing-immediately>

<https://mtlynch.io/code-review-love/>