
## 1. Requirements ~5min
- **Get interviewer buy in on goals and features**

**Functional requirements**
- Who is going to use it
- How are they going to use it?
- How are they not going to use it?

**Non functional requirements**
- How many users?
- What does system do?
- What are input/outputs?
- How much data do we need to handle?
- How many requests per second?
- What is expected read to write ratio?
- Consistency vs availability
## 1.1 Estimates
- **Get interviewer buy in on scope and define the non functional requirements**
- What is the throughput?
- What is the latency expected?
- What is the read and write ratio?
- What are the traffic estimates?
- What is the storage estimates?
- What is the memory estimates?
## 2. High level design
- **Get interviewer buy in on high level design**
- Whats the simplest design that will satisfy the functional requirements
- <https://excalidraw.com/>
- Sketch a high level design with main components
	- What are the core entities? Users, tweets, follows
	- What does APIs look like?
	- What does database schema look like?
	- What does algo look like?
	- What is the high level design for Read/Write scenario
- Why should high level design look like this?
- Useful thing to do is work back from API, so high level design develops as you go through each API design
## 3. Dive into component design
- Discuss the details of all the important core components.
- How are you storing the data?
- How will API, object oriented design look?
- How will you handle tricky area of ambiguity?
## 4. Scale the design
- What are the bottlenecks given the constraints?
- Do you need load balancers?
- Horizontal scaling?
- Caching?
- Database sharding?
## 5. Napkin math estimates
- Give an example of a napkin math estimate
- What is the throughput of each layer?
- What is the latency caused between each layer?
- What is the latency of a request?
- What is the max requests per seconds?

## 6. Wrap up
- What are system bottlenecks, whats next?
- Possible recap summary
- Handling error cases
- Operational handling
- Handling next scale curve

## Considerations
System design is your showcase of your technical leadership. They give you the opportunity to showcase your breadth and strengths. And call out what is outside your breadth of knowledge. The interview is about whether you can handle that kind of complexity without getting lost, without getting caught in the details and ensnared in the edges of the problem. The most important thing to do is to just keep going, you should never be like I'm not sure on what to do next. You gotta keep going. They are looking for technical leadership!

The interviewee needs to be the person who pushes the interview forward.

The point of the interviewer is to find the limit of what you're capable of.


### Appendix
- <https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#how-to-approach-a-system-design-interview-question>
- <https://bytebytego.com/courses/system-design-interview/a-framework-for-system-design-interviews>
- <https://gist.github.com/vasanthk/485d1c25737e8e72759f>
- <https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery>