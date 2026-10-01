# 90x card review

2401 cards are ready to publish. An automated gate read 2607 and objected to 456 of them (17%): 250 were rewritten and passed on the second look, 206 could not be saved and were dropped (8%). Mix by answer screen: 555 pick_one, 380 order, 344 tap_in_place, 217 bucket, 216 claim_grid, 195 match, 173 self_rate, 122 grid_toggle, 107 numeric, 92 assemble.

## What these are

90x is an interview-prep app. The Feed is being rebuilt around 47 question archetypes over ten answer screens (primitives). Every card names its archetype and its screen, and every answer is marked by a pure function against the answer definition shown below - no model, no typing. A reader answers without the lesson in front of them.

## What to judge

The gates already checked whether each card is correct, guessable and well-formed. This review asks the one question the gates cannot: **does this archetype earn a place in the Feed?** Judge each *kind* of question, not each individual card. For each archetype below, ask:

1. **Could a competent engineer who studied this topic answer it, with nothing else open?** A card that needs the lesson open is broken, however good it looks beside it.
2. **Does the answer screen fit the question?** Order for sequences, match for pairs, a number for a calculation, tap for a point inside a snippet.
3. **Are the why-step's wrong reasons plausible mistakes?** A right answer with an implausible reason is marked wrong, which punishes the reader for a writing failure.
4. **Was the gate right?** The rejected cards are at the end with its reasons.

Below: 81 cards, two per archetype, grouped by archetype so a *kind* of question can be judged as a whole. The two least-confident cards per archetype are shown, each with the lesson it came from and the answer definition the reader is graded against.

---

## Concept (`concept` · pick_one)

### 1. Lambda expressions · Easy

*java · gate confidence 0.8*

<sub>to object to this card: `## java-lambda-expressions` then `match: Which of the following statements about lambda expressions in Java is correct?`</sub>

**Question**

Which of the following statements about lambda expressions in Java is correct?

**Options**

A. A lambda expression can implement any interface, even one with multiple abstract methods.
B. A lambda expression always implements a functional interface, which has exactly one abstract method.
C. A lambda expression can be assigned to a variable of type Object without a cast.
D. A lambda expression can access and modify any local variable from the enclosing method.

**Answer (the reader is graded on)**

- Correct: B. A lambda expression always implements a functional interface, which has exactly one abstract method.

**Reference answer**

A lambda expression always implements a functional interface, which is an interface with exactly one abstract method. Default and static methods do not count toward that one abstract method.

**Graded on**

- A lambda expression implements a functional interface.
- A functional interface has exactly one abstract method.
- Default and static methods do not count toward the single abstract method.

<details><summary>The lesson this came from</summary>

A lambda expression is a syntactic construct that creates an instance of a functional interface by supplying the body of its single abstract method inline. The arrow operator separates an optional parameter list from a body, which can be a single expression or a block. Lambda expressions were introduced in Java 8 as a concise alternative to anonymous classes that implement exactly one method.

## Why interviewers ask this

Interviewers ask about lambdas to check whether you understand Java 8's shift toward passing behavior as data and how lambdas relate to functional interfaces. They probe target typing, capture rules, and the common java.util.function interfaces because those feed directly into streams and collection pipelines.

## The core idea

In Java, a lambda expression is the body of the one abstract method in a target functional interface. The compiler uses the expected type from the assignment, cast, or method argument to infer parameter types and check return compatibility. A lambda can capture local variables only if they are effectively final—never reassigned anywhere in their scope—but it can always read and modify instance fields and static fields. At runtime, the JVM uses invokedynamic and the LambdaMetafactory to create the call site rather than generating a separate anonymous class file at compile time. A lambda body may be a single expression whose value is returned automatically, or a block with explicit returns and statements.

## Key points

- A lambda expression always implements a functional interface, which has exactly one abstract method; default and static methods do not count toward that one.
- Target typing determines the lambda's type from the surrounding context—assignment, cast, or method argument—not from the lambda's own body.
- Parameter types may be omitted, a single untyped parameter may drop parentheses, and the body can be an expression returning a value or a block with statements and explicit returns.
- Captured local variables must be effectively final, meaning they are never reassigned anywhere in their scope, while instance fields and static variables may be read and modified freely.
- Common functional interfaces include Predicate<T> with boolean test(T), Function<T,R> with R apply(T), Consumer<T> with void accept(T), and Supplier<T> with T get().

## Your 60-second answer

A lambda expression is Java's concise syntax for implementing a functional interface inline. You write the parameter list, an arrow, and a body, and the compiler treats that as providing the single abstract method of whatever functional interface is expected at that spot. For example, `Runnable r = () -> System.out.println(42);` creates a Runnable without the boilerplate of an anonymous class. Lambdas matter because they let you pass behavior as data to methods like `forEach`, `filter`, and `map`, especially with the Streams API added in Java 8. One trade-off is that they can only target interfaces with exactly one abstract method, so if you need to implement two methods you still write an anonymous class. Another trade-off is captured local variables must be effectively final, which sometimes forces a workaround like using a single-element array or a field.

## If they dig deeper

**What is a functional interface, and how does @FunctionalInterface work?**

A functional interface is an interface with exactly one abstract method. Default and static methods do not count toward that one. The @FunctionalInterface annotation is optional but when present it makes the compiler fail if the interface has zero or more than one abstract method.

**Can you assign a lambda to Object or use var with it? Why not?**

No. A lambda expression needs a target type that is a functional interface because it supplies the body of that interface's single abstract method. Object has no abstract method, so the compiler cannot infer a functional interface; you need a cast like `(Runnable) () -> ...` or an explicit functional interface target such as a variable declaration.

**What are the rules for capturing variables in a lambda expression?**

Local variables and parameters from the enclosing method can be read only if they are effectively final—never reassigned anywhere in their scope. Instance fields and static fields can always be read and modified. A lambda cannot access default methods of the functional interface it implements because there is no interface instance `this` available inside the lambda.

**How does the JVM implement lambdas differently from anonymous inner classes?**

At compile time, the compiler emits an invokedynamic call site with a method handle to a synthetic private method containing the lambda body. At runtime, the LambdaMetafactory uses that method handle to generate or return a class implementing the functional interface; no separate class file is created for each lambda, unlike anonymous inner classes which generate a distinct class at compile time.

**What are the scoping differences between a lambda and an anonymous inner class?**

A lambda is lexically scoped: `this` and `super` refer to the enclosing instance, not the lambda object, and a lambda parameter cannot shadow a local variable from the enclosing method. An anonymous inner class has its own `this`, and its parameters and locals can shadow enclosing variables because it introduces a new nested scope.

## Worked example

Take `List<String> words = Arrays.asList("apple", "pear", "kiwi");` and the call `Collections.sort(words, (a, b) -> a.length() - b.length());`. The second argument's expected type is `Comparator<String>`, whose `compare` method takes two `String` parameters and returns `int`, so the compiler infers `a` and `b` as `String` and accepts the expression body as the returned difference. If you tried to assign that same lambda to a `Function<String, Integer>`—a one-parameter interface—the parameter count mismatches and compilation fails even though an int is returned. For capturing, `int limit = 5; List<Integer> xs = Arrays.asList(1, 2, 3); xs.replaceAll(x -> x * limit);` compiles because `limit` is never reassigned; adding `limit = 6` anywhere in the method makes `limit` not effectively final and the lambda will not compile. These two examples show target typing and effective final capture.

## Common traps

- Assigning a lambda to Object or using var without a functional interface target: compilation fails because a lambda has no independent type.
- Thinking a captured local variable can be reassigned as long as the reassignment happens before the lambda: any reassignment in scope breaks effective finality, even before the lambda is created.
- Conflating lambda with anonymous inner class for `this`: inside a lambda `this` is the enclosing object, not the lambda instance.
- Using a zero-argument lambda as a Consumer: Consumer's accept method takes one argument, so `() -> list.add(x)` targets a zero-argument void interface such as Runnable, not Consumer.

</details>

---

### 2. Strings · Easy

*java · gate confidence 0.8*

<sub>to object to this card: `## java-strings` then `match: Which statement about Java String is correct?`</sub>

**Question**

Which statement about Java String is correct?

**Options**

A. String is mutable, so methods like concat and replace modify the original object.
B. String is immutable, so methods like concat and replace return new String objects.
C. String is immutable, but methods like concat and replace modify the original object in place.
D. String is mutable, but methods like concat and replace return new String objects.

**Answer (the reader is graded on)**

- Correct: B. String is immutable, so methods like concat and replace return new String objects.

**Reference answer**

String is immutable, so methods like concat, replace, and substring return new String objects rather than modifying the original.

**Graded on**

- String is immutable; its content cannot change after construction.
- Methods that appear to modify text return new String instances.
- The original String remains unchanged after such calls.

<details><summary>The lesson this came from</summary>

In Java, a String is an immutable object representing a sequence of UTF-16 code units. Once constructed, its content cannot change; every method that appears to modify text, such as concat, replace, substring, and trim, returns a new String instead. The JVM stores string literals in a common string pool, so identical literals may share a single object. For mutable text, Java provides StringBuilder, which is not synchronized, and StringBuffer, which is synchronized.

## Why interviewers ask this

The interviewer is checking whether you understand Java's String behavior rather than just method names: immutability's consequences, the distinction between reference and content equality, string pool memory behavior, and when to switch to StringBuilder for performance. String manipulation questions also test boundary handling, index semantics, and algorithm design on character arrays.

## The core idea

Java keeps String immutable so that instances can be shared safely, hash codes stay stable, and strings can be used as keys without risk of change. Because of that, operations like `+` in a loop allocate and copy whole strings each iteration, so repeated concatenation should use StringBuilder. Content comparison uses equals, not `==`; `==` only checks whether two references point to the same object. Since Java 7, substring copies the underlying array rather than sharing the original, and since Java 9, strings may use a one-byte-per-character representation for Latin-1 text.

## Key points

- Java String objects are immutable: operations such as concat, replace, toLowerCase, and substring return new String instances rather than altering the original.
- String literals are automatically interned into a JVM string pool, so two identical literals can be `==` equal; `new String("x")` creates a distinct heap object.
- Use equals or equalsIgnoreCase for content comparison and compareTo for lexicographic order; `==` compares references, and Objects.equals avoids null checks.
- In loops, `result += part` creates a new String on every iteration and can be O(n²) overall; StringBuilder appends in amortized O(1) per append for typical use.
- substring(beginIndex, endIndex) returns characters from beginIndex inclusive to endIndex exclusive; charAt operates on UTF-16 code units, so a surrogate pair occupies two indexes.

## Your 60-second answer

In Java, String is immutable—once a String is constructed, its characters cannot be changed. Methods like concat, replace, and substring always return a new String, so you must assign the result back. String literals are stored in a JVM-wide string pool, so identical literals may be the same object, but == compares references, not text; use equals or compareTo for content. For repeated modification, use StringBuilder, which is mutable and not synchronized; StringBuffer is the thread-safe alternative but slower. One common performance trap is concatenating in a loop with +, because each iteration allocates and copies the whole string, giving quadratic time.

## If they dig deeper

**Why does Java make String immutable, and what concrete benefits does that provide?**

Once a String is created, its character content cannot change, which makes it safe to share across threads without synchronization. It also allows stable hash codes, so String works reliably as a HashMap key, and it prevents malicious or accidental mutation of security-sensitive values like file names or class names.

**How do `==`, `equals`, and `compareTo` differ for Java String comparison?**

`==` compares object references, so two different String objects with the same characters are not `==` unless they are the same interned instance. `equals` compares character content case-sensitively, `equalsIgnoreCase` ignores case, and `compareTo` returns a negative, zero, or positive integer based on lexicographic order of UTF-16 code units.

**What is the Java String pool, and when should intern() actually be used?**

The pool is JVM-managed storage that holds canonical String objects for literals; `intern()` returns the single canonical copy for a given character sequence. It is useful only when many equal strings will be compared repeatedly, because interned strings create entries in a shared pool and excessive use of dynamic strings can hurt lookup performance.

**How do you check whether two strings are rotations of each other?**

If they have the same length, concatenate the first string with itself and check whether the second string is a substring of that result. For example, `str1 + str1` contains `str2` exactly when one is a rotation of the other; the library `contains` or `indexOf` performs the search.

**Can you write an O(n) solution for the longest substring without repeating characters?**

Use two pointers with a Map from character to its most recent index. Move the right pointer forward, and when a repeat occurs, move the start index to max(current start, previous index + 1). Update the answer length right - start + 1 after each step; this scans the string once with O(1) map lookups, so O(n) time and O(min(alphabet size, n)) space.

## Worked example

Consider concatenation in a loop: `String result = ""; for (int i = 0; i < 5; i++) result += "a";` Each `+=` creates a new String object holding the old text plus the new character, and the previous intermediate object becomes garbage. For 5 items this is not noticeable, but for n characters the total copying is 0 + 1 + 2 + ... + (n-1) = n(n-1)/2 characters, so the loop is O(n²). Replacing it with `StringBuilder sb = new StringBuilder(); sb.append('a');` uses a mutable character buffer, amortizing growth to O(n) total, then `sb.toString()` produces one final immutable String.

## Common traps

- Comparing String contents with `==`; it only tests reference identity, so two `new String("x")` instances are `false`.
- Assuming methods like replace, trim, or toLowerCase mutate the original String; they return a new String and the original remains unchanged.
- Forgetting that substring's end index is exclusive, so `s.substring(0, 1)` returns only the first character, not two.
- Using `+` in a loop without realizing each concatenation creates and copies a whole new String, making the loop quadratic.

</details>

---

## Complexity (`complexity` · numeric)

### 3. Concurrency · Hard

*java · gate confidence 0.7*

<sub>to object to this card: `## java-concurrency` then `match: A ConcurrentHashMap in Java 8+ has 16 initial bins. Suppose `</sub>

**Question**

A ConcurrentHashMap in Java 8+ has 16 initial bins. Suppose 100 threads each insert 1000 distinct keys into the same map concurrently. What is the minimum number of CAS operations performed on empty bins during these insertions? Assume no resizing occurs and all keys hash to distinct bins.

**Answer (the reader is graded on)**

- 100000.0 ± 0.0

**Why (right answer, wrong reason is wrong)**

→ **A. Because each insertion into an empty bin requires a CAS to set the bin's first node, and there are 100,000 such insertions.**
  B. Because the map has 16 bins, so only 16 CAS operations are needed to initialize them, and subsequent insertions use synchronized blocks.
  C. Because each thread performs one CAS per bin it touches, so the total is 100 threads × 16 bins = 1,600 CAS operations.
  D. Because CAS is only used when a bin is empty, and with 100,000 keys and 16 bins, only 16 bins are ever empty, so 16 CAS operations occur.

**Reference answer**

The minimum number of CAS operations on empty bins is 100,000. Each of the 100,000 insertions (100 threads × 1000 keys) targets an empty bin, and inserting into an empty bin requires exactly one CAS operation. Since all keys hash to distinct bins and no resizing occurs, every insertion is into an empty bin, so the total CAS count equals the number of insertions.

**Graded on**

- In Java 8+, ConcurrentHashMap uses CAS to insert the first node into an empty bin.
- Each insertion into an empty bin performs exactly one CAS operation.
- With 100,000 total insertions and no collisions or resizing, the minimum CAS count is 100,000.

<details><summary>The lesson this came from</summary>

Java concurrency is the set of language features and library utilities for coordinating multiple threads that share memory. At the language level, synchronized, volatile, and wait/notify provide mutual exclusion, visibility, and condition waiting. The java.util.concurrent package adds higher-level constructs: ExecutorService for thread pools, Future and CompletableFuture for asynchronous results, Lock and atomic variables for non-blocking synchronization, and concurrent collections like ConcurrentHashMap and CopyOnWriteArrayList. The core challenge is preventing race conditions, memory visibility errors, and deadlocks while still using available CPU cores.

## Why interviewers ask this

Interviewers use Java concurrency questions to test whether you can reason about shared mutable state under contention. They look for knowledge of the Java Memory Model, the ability to choose the right synchronization primitive for a scenario, and familiarity with the standard library's concurrent utilities. A strong candidate explains not just what a construct does but when its trade-offs make it appropriate, such as preferring atomics over locks for simple counters.

## The core idea

All concurrency bugs boil down to three problems: atomicity (compound actions like check-then-act or read-modify-write being interrupted), visibility (one thread not seeing another's writes due to CPU caches), and ordering (compiler or CPU reordering instructions). Java's synchronization mechanisms establish happens-before relationships that constrain these three. For most application code, the highest-leverage tools are the java.util.concurrent abstractions: use ExecutorService instead of manually creating threads, use concurrent collections instead of synchronizing plain collections, and use atomics or locks for specific shared state. Understanding that a lock or volatile write does not just affect the locked variable but all writes before it in program order is the key to correct reasoning. Prefer higher-level constructs because they have been heavily tested and reduce the chance of subtle mistakes like forgetting to release a lock in a finally block.

## Key points

- The synchronized keyword provides both mutual exclusion and memory visibility; it is simpler than ReentrantLock but offers no tryLock, timed acquisition, or multiple condition variables.
- volatile guarantees visibility and ordering of a single field's reads and writes but does not make compound operations like count++ atomic.
- ExecutorService decouples task submission from thread creation; submit(Callable<T>) and submit(Runnable) both return a Future, and Future.get() throws ExecutionException wrapping the task's thrown exception.
- ConcurrentHashMap in Java 8+ uses per-bin synchronization and CAS for empty-bin insertion, allowing concurrent reads without locking the whole map.
- CopyOnWriteArrayList is thread-safe and ideal for read-mostly workloads because iterators see a stable snapshot, but each write copies the entire underlying array.

## Your 60-second answer

Java concurrency is about coordinating multiple threads that share data safely. The low-level tools are synchronized blocks, volatile fields, and wait/notify, but the java.util.concurrent package is usually the right choice: ExecutorService for thread pools, ConcurrentHashMap for a concurrent map, atomics for lock-free counters, and locks like ReentrantLock when you need features like tryLock or multiple condition queues. The fundamental problems are atomicity, visibility, and ordering; synchronized and volatile establish happens-before relationships that solve visibility and ordering, while locks and atomics solve atomicity. A key trade-off is that higher-level constructs like concurrent collections often provide better scalability at the cost of slightly weaker consistency guarantees, like weakly consistent iterators. In an interview, always mention that you would prefer an existing concurrent utility over hand-rolled synchronization unless there's a reason not to.

## If they dig deeper

**What is the difference between synchronized and ReentrantLock?**

Both provide mutual exclusion and memory visibility. ReentrantLock offers explicit lock/unlock, tryLock with timeout, lockInterruptibly, and multiple Condition objects for separate wait queues. synchronized is simpler and automatically releases on exit, even with exceptions, so it's preferred unless you need those extra capabilities.

**How does ConcurrentHashMap provide thread safety without locking the whole map?**

In Java 8+, it partitions the map into an array of bins. Writes to a bin synchronize on the bin's first node or use CAS for inserting into an empty bin. Reads are generally lock-free and see a weakly consistent view. When a bin becomes too large, it is converted to a tree bin to keep operations O(log n).

**What is a happens-before relationship in the Java Memory Model?**

It's a guarantee that if action A happens-before action B, then A's memory writes are visible to B and A's effects are not reordered with B. Common sources include synchronization lock/unlock, volatile writes/reads, Thread.start, Thread.join, and actions in the same thread. It is the foundation for reasoning about visibility and ordering without diving into hardware specifics.

**Explain CountDownLatch versus CyclicBarrier.**

CountDownLatch is a one-shot gate: one or more threads await until the count reaches zero, and it cannot be reset. CyclicBarrier is reusable and lets a fixed number of threads wait for each other to arrive at a common point; once all arrive, the barrier trips and can be reused. Latch is often used to wait for a set of tasks to complete, barrier for phased algorithms.

**How would you implement a bounded thread pool and why?**

Use ThreadPoolExecutor with corePoolSize, maximumPoolSize, a bounded BlockingQueue like ArrayBlockingQueue, and a rejection policy. Bounded pools prevent resource exhaustion under load, queue tasks to smooth bursts, and allow controlled degradation via rejection. Tuning queue size and pool size depends on whether tasks are CPU-bound or I/O-bound.

## Worked example

Two threads each increment a shared int counter 1000 times. The expression counter++ is not atomic: it reads the current value, adds one, and writes the result. If both threads read the same value, say 42, before either writes, both will write 43 and one increment is lost. The final count can be anywhere from 2 to 2000, often below 2000. Replacing int with AtomicInteger and using incrementAndGet() makes the read-modify-write a single atomic operation using compare-and-swap (CAS) in hardware. The final count is deterministically 2000. This illustrates why atomicity is separate from visibility and why the java.util.concurrent.atomic classes are the right tool for simple counters.

## Common traps

- Assuming volatile fixes all thread-safety issues, e.g., using volatile boolean flag for a compound check-then-act; volatile only ensures visibility of the flag, not the atomicity of the whole operation.
- Using Thread.stop() or Thread.destroy() to terminate threads; these are deprecated and unsafe because they release locks and can leave objects in inconsistent states. Use interruption instead.
- Wrapping every read/write in synchronized when a concurrent collection would be more scalable; for example, using Collections.synchronizedList for a read-heavy list instead of CopyOnWriteArrayList.
- Forgetting that Future.get() throws ExecutionException, not the task's exception directly, so you must unwrap the cause to find the original error.

</details>

---

### 4. OOP Concepts · Hard

*java · gate confidence 0.7*

<sub>to object to this card: `## java-oop-concepts` then `match: Consider a Java class hierarchy with an abstract base class `</sub>

**Question**

Consider a Java class hierarchy with an abstract base class Shape and two concrete subclasses Circle and Square. Each subclass overrides the abstract method area(). At runtime, the JVM uses a virtual method table (vtable) per class to dispatch calls. For a call site shape.area() where shape is declared as Shape, what is the minimum number of memory indirections (pointer dereferences) required to reach the correct method implementation, assuming the object reference is already in a register and the vtable is laid out contiguously with the method pointer at a fixed offset?

**Answer (the reader is graded on)**

- 2.0 ± 0.0

**Why (right answer, wrong reason is wrong)**

  A. Because the JVM stores the method pointer directly in the object header, so only one dereference is needed.
→ **B. Because the vtable pointer is stored in the object, and the method pointer is stored in the vtable, requiring two dereferences.**
  C. Because the JVM uses inline caching, which eliminates all indirections after the first call.
  D. Because the method pointer is stored in the class object, and the class object is reached via the object's class word, requiring three dereferences.

**Reference answer**

The minimum number of memory indirections is 2: one to load the object's vtable pointer from the object header, and one to load the method pointer from the vtable at the fixed offset for area().

**Graded on**

- Dynamic dispatch requires reading the object's vtable pointer, then reading the method entry from that vtable.
- The object reference itself is already in a register, so dereferencing it to get the vtable pointer is the first indirection.
- The second indirection fetches the actual method address from the vtable.
- This is the standard two-level indirection used by JVM implementations for virtual method dispatch.

<details><summary>The lesson this came from</summary>

Object-oriented programming organizes code into classes that bundle state (fields) with behavior (methods). In Java, classes act as blueprints, instance fields hold per-object state, and methods operate on that state. The four core principles are encapsulation (restricting access to internal state), inheritance (subclassing a parent type), polymorphism (dispatching calls based on the actual object's runtime type), and abstraction (exposing only essential behavior through abstract classes and interfaces).

## Why interviewers ask this

Interviewers use OOP questions to test whether you can design cohesive classes, protect invariants with access control, and explain runtime dispatch versus compile-time resolution. They also probe Java-specific mechanics—single inheritance, interfaces, Object methods, and where Java is not purely object-oriented—so a candidate who only recites definitions fails. Strong answers connect each principle to a concrete Java feature or failure mode.

## The core idea

OOP binds data and the operations on it into one unit, so an object's state changes only through its methods. Encapsulation is enforced in Java with access modifiers: private fields hide representation, protected exposes to subclasses and the package, and public methods provide behavior. Inheritance allows a subclass to reuse a parent's fields and methods; Java permits exactly one superclass but many interfaces. Polymorphism means a variable of type Shape can hold a Circle, and a call like shape.area() executes Circle's override using the runtime class's method table. Abstraction lets abstract classes and interfaces declare what an object does without committing to how. Java is not purely OOP because primitives and static members exist outside objects.

## Key points

- In Java, private fields plus public methods are the standard encapsulation mechanism, and protected means accessible within the package and subclasses.
- Java implements polymorphism through dynamic dispatch: overridden instance methods are resolved from the object's runtime class, not the reference's declared type.
- A Java class can extend only one superclass but can implement any number of interfaces; default methods can cause conflicts that must be explicitly resolved.
- Every Java class implicitly extends Object, so all objects inherit equals, hashCode, toString, getClass, and thread coordination methods like wait and notify.
- Java is not purely object-oriented because primitives (int, boolean, double) and static members can be used without any object instance.

## Your 60-second answer

Object-oriented programming in Java means designing programs as objects that combine state (fields) and behavior (methods). The four core ideas are encapsulation, inheritance, polymorphism, and abstraction. Encapsulation hides internal state behind private fields and exposes behavior through public methods, which protects invariants. Inheritance lets a class extend one superclass and inherit its fields and methods, while interfaces allow multiple type contracts. Polymorphism means a superclass or interface reference can point to a subclass object, and the JVM dispatches the overridden method based on the actual object's runtime type, not the reference type. Abstraction uses abstract classes and interfaces to define what an object does without specifying how. The trade-off is that inheritance creates tight coupling, so composition is often preferred for flexibility; Java is considered not purely OOP because primitives and statics live outside the object model.

## If they dig deeper

**When can an object reference be cast to a Java interface reference?**

An object reference can be cast to an interface type when the object's actual runtime class implements that interface. The JVM checks the cast at runtime and throws ClassCastException if the object does not implement it; upcasting to an interface is implicit, while casting back to a concrete class requires an explicit cast. This is the basis of programming to interfaces.

**What is the difference between an abstract class and an interface in Java?**

An abstract class can have instance fields, constructors, and concrete methods, so it can carry shared state and enforce a base implementation. An interface primarily declares a contract, though since Java 8 it can have default and static methods, and since Java 9 private methods. A class extends one abstract class but can implement many interfaces, so use an interface for a capability and an abstract class for shared implementation.

**Why is Java not considered a purely object-oriented language?**

Java has primitive types like int, boolean, and double that are not objects, and static variables and methods can be used without any instance. Operations on primitives and static calls are not dispatched through objects. Java intentionally kept primitives for performance and uses wrapper classes only when objects are needed.

**What methods does java.lang.Object define, and why must equals and hashCode be overridden together?**

Object defines getClass, hashCode, equals, toString, clone, and wait/notify/notifyAll; finalize was deprecated in Java 9. The contract requires equal objects to have equal hash codes, so if you override equals to compare fields, you must override hashCode consistently. Otherwise HashMap and HashSet lookups fail for equal objects that hash differently.

**How can you create an object without the new operator, and when is that appropriate?**

You can use reflection with Class.forName(...).getDeclaredConstructor().newInstance(), call clone() on a class that implements Cloneable, deserialize via ObjectInputStream, or load a class and instantiate it with a class loader. Reflection is slower and less type-safe, clone makes shallow copies unless overridden, and deserialization can bypass constructors and leave invariants uninitialized. Prefer new unless you need runtime plugin loading, copying, or persistence.

## Worked example

Consider an abstract class Shape with an abstract method area(). A Circle stores a radius and overrides area to return Math.PI * radius * radius; a Square stores a side and returns side * side. A method printArea(Shape s) prints s.area(). Calling printArea(new Circle(2)) prints 12.57 because the compiler only knows s is Shape, but at runtime the JVM looks up area in Circle's method table. Calling printArea(new Square(3)) prints 9.0 through the same call site. Adding a Triangle later requires no changes to printArea, which shows polymorphism making code open for extension without modifying existing behavior.

## Common traps

- Confusing overloading with overriding: overload resolution happens at compile time based on argument types, while overriding dispatches at runtime based on the object's class.
- Claiming Java is purely object-oriented when primitives and static members exist outside instances.
- Overriding equals without hashCode, which breaks HashMap and HashSet because equal objects must hash equally.
- Thinking Java supports multiple inheritance because it has interfaces; a class still extends only one superclass, and default method conflicts must be resolved explicitly.

</details>

---

## Which approach (`which-approach` · pick_one)

### 5. Rate limiting · Hard

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-rate-limiting` then `match: You are designing a rate limiter for a distributed API with `</sub>

**Question**

You are designing a rate limiter for a distributed API with strict enforcement requirements: the limit must never be exceeded, even during bursts or at window boundaries, and the system must continue to enforce limits correctly when the shared state store (Redis) is temporarily unavailable. Which approach should you use?

**Options**

A. Fixed window counter with fail-open policy
B. Sliding window log with fail-closed policy
C. Token bucket with fail-open policy
D. Leaky bucket with fail-closed policy

**Answer (the reader is graded on)**

- Correct: B. Sliding window log with fail-closed policy

**Why (right answer, wrong reason is wrong)**

→ **A. Sliding window log tracks all request timestamps in the trailing window, so at any moment the count reflects exactly the requests in that window, preventing boundary bursts.**
  B. Sliding window log is more memory-efficient than fixed window, so it can store more counters and enforce limits more strictly.
  C. Fail-closed policy is simpler to implement than fail-open, so it is more reliable during store outages.
  D. Sliding window log uses atomic operations in Redis, which are faster than fixed window increments, ensuring no requests are missed.

**Reference answer**

Use a sliding window log or counter with a fail-closed policy. Sliding window algorithms prevent the boundary burst that fixed windows allow, and fail-closed ensures limits are preserved during store outages by rejecting requests rather than allowing unlimited traffic.

**Graded on**

- Sliding window log/counter enforces the limit over a trailing window, preventing boundary bursts.
- Fail-closed rejects requests when the store is unavailable, preserving strict limits.
- Fixed window can allow up to 2x the limit at boundaries, violating strict enforcement.
- Fail-open would allow requests during store outages, potentially exceeding limits.

<details><summary>The lesson this came from</summary>

Rate limiting enforces a maximum number of requests a client may make within a defined period before requests reach a protected service. It keeps per-client state—counters, tokens, or timestamps—and rejects, throttles, or queues requests that exceed the limit, usually returning HTTP 429 with Retry-After headers. The enforcement point is typically an API gateway, load balancer, edge proxy, or a service-level middleware.

## Why interviewers ask this

Interviewers use this question to test whether you can design a high-throughput, correct limiter under real constraints: choosing identifier, algorithm, storage, and fault tolerance. Amazon, Uber, Atlassian, and Patreon have asked 'Design an API Rate Limiter,' so they expect discussion of distributed state and race conditions rather than a single-node counter.

## The core idea

The central mechanism is per-client state updated atomically on every request, then compared against a threshold for the current window. Token bucket and leaky bucket smooth bursts; fixed window counters are cheap but allow doubled traffic at boundaries; sliding window/log counters are more accurate and more expensive. In a distributed system, state must live in a shared store such as Redis because a client can hit different nodes; read-modify-write must be atomic to avoid races. Fault tolerance is a policy choice: fail-open preserves availability but can let a thundering herd through, while fail-closed preserves limits but can block legitimate traffic during an outage.

## Key points

- Choose identity from API key, authenticated user ID, or IP; IP alone misidentifies users behind NATs or proxies.
- Fixed window counters permit up to 2× the configured limit across a boundary, while sliding window/log algorithms eliminate that burst but need more state.
- In a distributed deployment, per-node counters are insufficient; a shared store such as Redis with atomic Lua scripts or increment operations keeps a global view.
- The limiter should return standard headers such as X-RateLimit-Remaining, X-RateLimit-Reset, and Retry-After, and use status 429.
- Fault tolerance is explicit: fail-open keeps service available but ineffective during store outages; fail-closed preserves limits but may reject all traffic.

## Your 60-second answer

A rate limiter caps how many requests a client can make in a time window to protect the backend from overload and abuse. I'd identify the client by API key, user ID, or IP, and enforce the limit at the API gateway or a middleware layer. For the algorithm, token bucket is a good default because it allows a configurable burst while enforcing average rate; a sliding window gives stricter enforcement if precision matters. In a distributed system, I'd keep counters in Redis or another shared store, using atomic operations so concurrent nodes don't race. If Redis is down, I need a fault-tolerance decision: fail-open to keep serving, or fail-closed to preserve limits. I'd return 429 with Retry-After and rate-limit headers so clients can back off.

## If they dig deeper

**How do you identify users to rate limit?**

Start with the strongest available identity: authenticated user ID or API key. Fall back to IP for anonymous traffic, but note that many users can share a NAT IP and attackers can rotate IPs, so IP limits should be more permissive or combined with other signals.

**What algorithm do you use for rate limiting?**

For general APIs I would use token bucket because it supports controlled bursts and has minimal state: each client stores a token count and last refill time. If the requirement is strict no-burst pacing, leaky bucket or a sliding window counter enforces a smoother rate. Fixed window is simplest but I would avoid it unless the boundary-up-to-2x burst is acceptable.

**How do you scale this in a large distributed website?**

Use a centralized rate-limit store such as Redis, with per-client keys and TTLs. Gateway nodes run an atomic Lua script that checks and increments the counter in one round trip, avoiding race conditions. For extreme scale, shard Redis keys by client hash, use local caches for hot limits, and accept eventual consistency where precise global accuracy is not required.

**How do you make your rate limiter fault tolerant?**

The limiter needs a policy for store failure. A common choice is fail-open with a local fallback counter or a degraded limit, preserving availability at the risk of overload. Fail-closed is safer for abuse protection but will block all traffic if Redis goes down. Whichever I choose, I add monitoring, alerts, client Retry-After headers, and replication for the store.

## Worked example

Set a fixed-window limit of 100 requests per minute. A client sends 100 requests in the final second of minute 1, at 12:00:59. The minute-1 counter reaches 100 and the next request in that second is denied. At 12:01:00 the fixed window resets; the client sends another 100 requests, all allowed, so 200 requests pass in about two seconds. A sliding-window implementation instead checks the trailing 60 seconds: at 12:01:00 it still observes the 100 requests from 12:00:59 and denies the new one because the count would become 101. The old requests stop counting only after 12:01:59, so the client cannot double the limit at the boundary.

## Common traps

- Using per-node in-memory counters instead of a shared store in a multi-node service, which lets clients route around the limit.
- Implementing counters with non-atomic read-modify-write in Redis, so concurrent requests can pass when they should be rejected.
- Picking fixed window without explaining that the limit can be exceeded at boundaries.
- Omitting the failure mode; if the store fails, an unstated default can silently allow all traffic or take the API down.

</details>

---

### 6. Sharding strategies · Hard

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-sharding-strategies` then `match: You are designing a sharded database for a ride-hailing serv`</sub>

**Question**

You are designing a sharded database for a ride-hailing service. The primary table stores trips, keyed by trip_id, which is a UUID generated at trip creation. The dominant query pattern is: (1) point lookups by trip_id to fetch trip details, and (2) range queries over start_time to retrieve all trips that started within a time window for analytics. You must choose a sharding strategy. Which approach best balances these requirements?

**Options**

A. Hash sharding on trip_id
B. Range sharding on start_time
C. Directory-based sharding with trip_id as the lookup key
D. Range sharding on trip_id

**Answer (the reader is graded on)**

- Correct: A. Hash sharding on trip_id

**Why (right answer, wrong reason is wrong)**

→ **A. Hash sharding on trip_id ensures that point lookups by trip_id are routed to a single shard without an extra lookup, while range queries over start_time can be parallelized across shards and merged, which is acceptable for analytics.**
  B. Hash sharding on trip_id makes range queries over start_time efficient because the hash function preserves the order of start_time values.
  C. Hash sharding on trip_id avoids hot shards because trip_id is a UUID, which is monotonically increasing.
  D. Hash sharding on trip_id eliminates the need for a directory service, which is the only way to support range queries.

**Reference answer**

Hash sharding on trip_id is the best choice. Point lookups by trip_id are the most frequent and latency-sensitive, and hash sharding provides uniform distribution and direct routing for them. Range queries over start_time will fan out to all shards, but they are analytics queries that can tolerate higher latency and can be executed in parallel. Range sharding on start_time would make range queries efficient but would create a hot shard on the most recent time range and would not support efficient point lookups by trip_id. Directory-based sharding adds an extra hop for every point lookup and introduces a critical lookup service dependency without solving the range query problem better than hash sharding.

**Graded on**

- Hash sharding on trip_id gives uniform distribution and direct point lookups.
- Range queries over start_time fan out to all shards but are acceptable for analytics.
- Range sharding on start_time would create a hot shard and hurt point lookups.
- Directory-based sharding adds latency and a single point of failure without clear benefit.

<details><summary>The lesson this came from</summary>

Sharding strategies decide which physical shard stores a row or record by mapping a partition key to a shard. Range sharding assigns contiguous key intervals to shards; hash sharding applies a hash function and maps the hash to a shard; directory-based sharding keeps a separate lookup service that resolves keys to shard locations at request time. These are horizontal partitioning schemes: every shard holds the same schema and a subset of rows.

## Why interviewers ask this

The interviewer wants to see whether you can choose a partitioning strategy that keeps data balanced and supports the actual query patterns, then explain the operational cost of rebalancing and cross-shard access. In the evidence, it shows up in designing a marketplace, migrating data, and building a key-value store, where distribution directly affects latency, availability, and consistency.

## The core idea

The core choice is between predictable key ranges and balanced load. Range sharding gives contiguous key order, which helps range scans but concentrates writes when keys are monotonic like timestamps. Hash sharding spreads keys uniformly and is good for point lookups, but a range query must fan out to all shards. Directory-based sharding inserts a lookup service between clients and physical shards, so the mapping can change without changing application code, at the cost of an extra hop and a critical lookup component.

## Key points

- Range sharding assigns each shard a contiguous interval of the shard key, such as user IDs 1 to 1 million, so range scans over that key stay on one shard but skewed intervals create hot shards.
- Hash sharding uses a hash function over the shard key and maps the result to a shard, giving uniform distribution for point lookups while scattering adjacent keys across all shards.
- Directory-based sharding uses an external lookup service to map a shard key to a physical node, allowing shards to be added or remapped without changing application code, but the lookup service is an extra dependency and a potential single point of failure.
- Rebalancing range shards is done by splitting or moving existing ranges, while hash sharding typically needs consistent hashing or a hash-ring scheme to avoid remapping most keys when nodes change.
- Vertical partitioning splits columns into different tables or servers, whereas horizontal sharding splits rows; the term sharding normally refers to the horizontal row-based case.

## Your 60-second answer

Sharding strategies determine which physical database node owns a row by mapping a partition key to a shard. The three main strategies are range, hash, and directory-based. Range sharding assigns contiguous key intervals to shards, so range scans are efficient, but monotonic keys such as timestamps can overload the last shard. Hash sharding hashes the shard key and uses the hash to select a shard; it balances data well and is excellent for point lookups, but range queries must fan out to every shard. Directory-based sharding uses a separate lookup service that tells the client which shard holds a given key, which makes adding shards or changing the mapping easier, but it adds an extra network hop and a lookup service that must be highly available. In practice, I pick the strategy based on the dominant query pattern and key distribution, and combine sharding with replication for fault tolerance.

## If they dig deeper

**How do you choose a good shard key?**

Pick a key that appears in most queries, has high cardinality, and is not monotonically increasing unless you deliberately want range locality. For point lookup workloads, a user ID or item ID works; for time-series data, a timestamp plus another dimension can avoid a single hot shard.

**Why does hash sharding break range scans?**

A hash function distributes adjacent keys pseudo-randomly across shards, so keys that are consecutive before hashing rarely land on the same shard. A range query must therefore fan out to every shard, merge partial results, and usually cannot use a single-shard index efficiently.

**What actually happens when you add a shard to a hash-based system?**

With simple modulo hashing, almost every key remaps, so nearly all data must move and writes often have to pause. Consistent hashing avoids this by assigning each node one or more positions on a ring and mapping each key to the next position, so adding one node moves only the keys in that node's segment, typically a small fraction.

**How do you handle cross-shard queries such as joins or global ordering?**

The application or query layer splits the query, sends it to relevant shards, and merges results. For joins, you either denormalize so the join is unnecessary, co-locate related entities on the same shard using the same key, or run a distributed join that is expensive and should be rare. Global ordering requires merging sorted partial results from all shards.

**How do you prevent the directory service in directory-based sharding from becoming a single point of failure?**

Replicate the directory across multiple nodes and use a consensus protocol such as Raft or Paxos to keep replicas consistent, or push a cached copy to clients and invalidate it on remapping. The directory's availability and consistency must be designed as carefully as the database itself, including handling stale mappings and split-brain scenarios.

## Worked example

Take 100 million users with IDs from 1 to 100 million. Range sharding could put IDs 1 to 25 million on shard A, 25 million to 50 million on shard B, 50 million to 75 million on shard C, and 75 million to 100 million on shard D. A lookup for user 40,000,123 goes directly to shard B without scanning, and a query for users 45 million to 55 million touches only shards B and C. Because new user IDs are assigned from a monotonically increasing sequence, all writes eventually concentrate on shard D, making it hot while shard A remains idle. Hash sharding with consistent hashing instead maps each user ID to a position on a large ring, such as 0 to 2^63 minus 1; nearby IDs land far apart, so writes spread across all four shards. Adding shard E then remaps only the keys whose ring positions fall in E's segment, moving roughly one share of the data in the uniformly distributed case rather than the whole dataset.

## Common traps

- Using range sharding with a monotonically increasing key without pre-splitting or range rotation, which funnels writes to a single shard.
- Assuming hash sharding supports efficient range queries; it usually scatters adjacent keys and forces a fan-out.
- Overlooking the directory service availability in directory-based sharding and treating the lookup layer as a trivial component.
- Mixing up vertical partitioning with sharding: sharding splits rows, while vertical partitioning splits columns.

</details>

---

## What breaks first (`what-breaks-first` · pick_one)

### 7. Consistent hashing · Hard

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-consistent-hashing` then `match: A distributed cache uses consistent hashing with 100 physica`</sub>

**Question**

A distributed cache uses consistent hashing with 100 physical nodes, each with 10 virtual nodes, and stores 1,000,000 keys. The hash function is uniform, and all nodes have equal capacity. A new physical node is added with 10 virtual nodes. Under these assumptions, what breaks first as the system scales to 10,000 physical nodes with the same per-node virtual node count?

**Options**

A. Load imbalance among physical nodes becomes severe because some nodes own many more keys than others.
B. The number of keys remapped when a node joins grows to nearly all keys, causing massive cache misses.
C. The ring's metadata and routing state grows linearly with the number of virtual nodes, becoming the first bottleneck.
D. Replication factor must be increased to maintain availability, causing write amplification.

**Answer (the reader is graded on)**

- Correct: C. The ring's metadata and routing state grows linearly with the number of virtual nodes, becoming the first bottleneck.

**Why (right answer, wrong reason is wrong)**

→ **A. Because each virtual node requires its own hash value and owner mapping, and with 100,000 vnodes the memory and update overhead dominates before load imbalance appears.**
  B. Because virtual nodes are stored in a distributed hash table that requires O(V) network hops per lookup, making routing the bottleneck.
  C. Because the hash function becomes non-uniform when the number of vnodes exceeds 65,536, causing hot spots.
  D. Because adding a physical node with 10 vnodes causes 10% of all keys to be remapped, overwhelming the network.

**Reference answer**

The ring's metadata and routing state grows linearly with the number of virtual nodes, so at 10,000 physical nodes with 10 vnodes each, the system must maintain 100,000 ring positions. This increases memory usage, update propagation overhead, and the cost of finding a key's successor, making metadata management the first bottleneck before load imbalance or remapping cost.

**Graded on**

- Virtual nodes multiply the number of ring positions: 10,000 physical nodes × 10 vnodes = 100,000 positions.
- Each position requires metadata (hash value, owner node) and must be updated on membership changes.
- Lookup cost grows with the number of positions, typically O(log V) with a sorted structure, but memory and update overhead scale linearly.
- With uniform hashing and equal capacity, load imbalance is not the first issue; the sheer number of vnodes strains metadata management.

<details><summary>The lesson this came from</summary>

Consistent hashing is a distributed hashing scheme that places both object keys and server/node identifiers into the same circular hash space using a hash function. A key is assigned to the first node encountered when moving clockwise from the key's position on the ring. When a node is added or removed, only the keys that fall between that node and its immediate predecessor or successor are remapped, which is about K/N of all keys for N nodes and K keys. Virtual nodes can be added to give each physical node multiple ring positions for more even load.

## Why interviewers ask this

Interviewers ask this when evaluating sharding, distributed caches, or any system where the node set changes under load. They test whether you know simple modulo hashing breaks on scale, and whether you can explain ring assignment, remapping cost, and how virtual nodes fix imbalance.

## The core idea

A modulo scheme `server = hash(key) % n` couples every key to the current node count, so changing n invalidates most mappings. Consistent hashing decouples key placement from the count by hashing keys and nodes into one fixed ring and assigning each key to the next node clockwise. With uniform hashing, roughly K/N keys move when the node set changes, rather than almost all K keys. Virtual nodes give each physical node many positions on the ring to reduce the variance from a few unlucky hash positions, though they increase the number of ring intervals to manage.

## Key points

- With simple modulo hashing `hash(key) % N`, changing N remaps nearly all keys, while consistent hashing remaps only about K/N keys on average.
- Consistent hashing hashes both keys and nodes into the same circular space; a key is assigned to the first node encountered clockwise.
- Virtual nodes map one physical node to multiple ring positions, smoothing load and reducing hot spots at the cost of more state.
- Apache Cassandra's default partitioner uses consistent hashing with vnodes; the original Dynamo design used a ring, but DynamoDB itself does not.
- Replication on a ring is often done by placing copies on the next distinct physical nodes clockwise, subject to a replication factor and placement policy.

## Your 60-second answer

Consistent hashing is a key-to-node assignment scheme that minimizes remapping when the node set changes. Instead of computing a server with `hash(key) % n`, you hash both keys and servers into the same circular space and assign each key to the first server clockwise from it. With n servers, an average of about 1/n of keys move when a server is added or removed, compared with modulo hashing where nearly every key can move. To prevent hot spots from uneven ring positions, each physical server is given several virtual node positions; that spreads load but adds mapping overhead. Replicas are often placed on the next distinct servers clockwise. Apache Cassandra's default partitioner uses this approach, and the original Dynamo design used a ring, although DynamoDB now uses a different routing layer.

## If they dig deeper

**How many keys move when a new node joins a consistent hash ring with N existing nodes and K keys?**

On average about K/N keys move, because the new node only takes over the interval between its predecessor and itself. With a bad hash distribution or no virtual nodes, the actual number can be much larger.

**Why are virtual nodes needed, and what is the downside?**

Virtual nodes create many ring positions per physical node, so each node owns many small intervals and load variance shrinks. The downside is more token/state entries to store and update, and more segments to consider for replication.

**How does replication usually work on the ring?**

A key is written to the owner node and then to the next N-1 distinct physical nodes clockwise. The placement must skip additional vnodes belonging to the same physical host; otherwise multiple replicas can land on one machine.

**What happens if all node positions happen to cluster in one arc of the ring?**

The nodes in that arc will receive almost all keys, regardless of node count. Virtual nodes with a well-distributed hash mitigate this, but there is still a nonzero probability of imbalance; some systems also use bounded loads or capacity-aware assignment.

**How does Apache Cassandra actually use consistent hashing today, and how does that differ from the original Dynamo ring?**

Cassandra's Murmur3Partitioner hashes partition keys into a 64-bit ring and assigns each node multiple vnodes. The original Dynamo paper also used consistent hashing with virtual nodes and gossip, but DynamoDB as an AWS service does not expose a ring; its request router maps partitions to storage nodes through internal metadata.

## Worked example

Take a ring with range 0-99 and four nodes A, B, C, D at positions 10, 30, 60, 90. Keys k1, k2, k3, k4 have hash values 5, 15, 45, 75. Clockwise assignment gives k1->A (wrap from 5 to 10), k2->B (15 to 30), k3->C (45 to 60), k4->D (75 to 90). Add node E at position 15. Only k2 changes: from position 15, the next clockwise node is now E instead of B. The other three keys still hit A, C, and D. With modulo hashing, converting from %4 to %5 on the same raw hash values 5, 15, 45, 75 would map all four keys to index 0 in the five-node scheme, so every key moves.

## Common traps

- Claiming Amazon DynamoDB uses a consistent hashing ring: the original Dynamo paper used ring/vnodes, but DynamoDB itself routes via internal metadata, not a ring.
- Saying consistent hashing moves only O(1) keys: the expected number of remapped keys is K/N, and it can be more with poor hash distribution.
- Confusing virtual nodes with replicas: virtual nodes are extra ring points for one physical node for balance, not copies of data.
- Describing replication as 'the next three nodes clockwise' without requiring distinct physical hosts; adjacent vnodes may belong to the same machine and must be skipped.

</details>

---

### 8. Design a web crawler · Hard

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-design-a-web-crawler` then `match: You are designing a web crawler with a URL frontier, fetcher`</sub>

**Question**

You are designing a web crawler with a URL frontier, fetchers, parsers, and a visited store. The visited store is a distributed key-value store keyed by canonical URL. You add a Bloom filter in front of the visited store to reduce lookups. Under a sustained crawl with many new URLs, which component is most likely to become the bottleneck first, assuming standard implementations and no extra memory?

**Options**

A. The URL frontier, because it must prioritize and schedule URLs across many domains.
B. The fetchers, because they are I/O-bound and limited by network bandwidth.
C. The parsers, because extracting links from HTML is CPU-intensive.
D. The visited store, because every new URL requires a lookup and possibly a write.

**Answer (the reader is graded on)**

- Correct: D. The visited store, because every new URL requires a lookup and possibly a write.

**Why (right answer, wrong reason is wrong)**

  A. The visited store is a single point of consistency; all fetchers must query it before fetching, creating a serialization point.
  B. The visited store must store the full URL and metadata, so its storage capacity is exhausted quickly.
  C. The visited store is updated on every fetch, so write amplification causes it to slow down.
→ **D. The visited store is queried for every extracted URL, and with many new URLs, the request rate exceeds its throughput.**

**Reference answer**

The visited store is most likely to become the bottleneck first. Every new URL requires a canonicalization and a lookup in the distributed key-value store to determine if it has been seen. With many new URLs, this store receives a high volume of read and write requests, and its latency and throughput become the limiting factor. The Bloom filter reduces some lookups but cannot eliminate them, and false positives still require store checks.

**Graded on**

- Every extracted URL must be checked against the visited store before enqueueing.
- The visited store is a distributed key-value store, which has finite throughput and latency.
- A Bloom filter reduces lookups but does not eliminate them; false positives still hit the store.
- Fetchers and parsers are stateless and horizontally scalable, so they are less likely to be the first bottleneck.

<details><summary>The lesson this came from</summary>

A web crawler is a distributed system that systematically downloads web pages by following hyperlinks, extracts new URLs from each page, and stores raw or parsed content for indexing or other processing. Its core components are a URL frontier (priority queue), fetchers that respect per-domain politeness, a parser/link extractor, and a deduplication store keyed by canonical URL to avoid re-fetching and duplicate content.

## Why interviewers ask this

This question tests whether you can design a horizontally scalable, I/O-bound system with unbounded input, where fairness, politeness, deduplication, and prioritization are all driven by distributed data structures. Interviewers probe how you handle scale, stale data, and respecting external sites while keeping crawl throughput high.

## The core idea

A crawler treats the web as a graph: pages are nodes and links are edges. The URL frontier is a priority queue that emits next URLs to fetch; fetchers download pages and parsers extract outlinks. Each outlink is canonicalized and checked against a distributed seen-URL store before enqueueing. A politeness manager throttles requests per domain using robots.txt and per-domain timestamps. Horizontal scaling comes from partitioning the frontier and visited store by URL hash and running many stateless fetchers. Re-crawling reinserts URLs based on change frequency, and the system is eventually consistent.

## Key points

- The URL frontier is a priority queue; it orders URLs by importance and schedules per-domain to enforce politeness and fairness.
- URL deduplication requires a canonical form (lowercase scheme and host, remove default ports and fragments, resolve relative URLs) and a distributed visited store keyed by that form.
- A Bloom filter may reduce dedup store lookups, but if it is used for visited-set membership, false positives cause new URLs to be incorrectly skipped; the authoritative store must still decide admissions.
- Politeness enforcement combines robots.txt disallow/crawl-delay with per-domain concurrency limits and last-request timestamps, often in Redis.
- Re-crawling is scheduled by estimating change frequency and inserting URLs back into the frontier when their earliest-next-fetch time passes.

## Your 60-second answer

I'd design a distributed web crawler with four main parts: a URL frontier, fetchers, parsers, and a visited store. The frontier is a priority queue that schedules URLs both by importance and by per-domain politeness. A fetcher takes a URL from the frontier, checks robots.txt, downloads the page, and hands it to a parser. The parser extracts outlinks, canonicalizes them—lowercase scheme and host, remove default ports and fragments—and checks the visited store before enqueueing new URLs. The visited store is a distributed key-value store keyed by canonical URL; a Bloom filter can reduce lookups but cannot be the source of truth because false positives skip new URLs. Content is stored with a fingerprint to dedup identical pages. Trade-off: a purely periodic crawler is simpler, but adding a backend for near-real-time high-priority pages increases freshness at the cost of scheduling complexity.

## If they dig deeper

**Should it be real-time or periodic?**

Start with periodic batch crawls; they are simpler and easier to reason about. Real-time or near-real-time crawling can be layered later by using the frontier as a continuously fed priority queue and scheduling high-priority sources sooner, but it couples the crawler to the indexing freshness requirements. I'd ask about freshness SLAs before choosing.

**How do you handle URL deduplication and track visited vs unvisited URLs?**

First canonicalize the URL: lowercase scheme and host, remove default ports, strip fragments, and resolve relative paths. Query parameter order should only be normalized if we know the site treats it as order-insensitive; otherwise leave it. Store canonical URLs in a distributed key-value store with statuses like discovered, queued, fetching, done, failed. A Bloom filter can front the store to reduce lookups, but if it is used to test membership in the visited set, its false positives will incorrectly mark new URLs as seen; the authoritative store must decide admission.

**How do you implement delay between requests to the same domain?**

Maintain per-domain state in Redis: last fetch timestamp and current concurrent request count. Before fetching, a worker asks a politeness manager; it checks robots.txt disallow rules and crawl-delay, and ensures the domain is below its concurrency limit. If the next allowed time has not arrived, the URL is returned to the frontier with that time as the earliest fetch time.

**How do you prioritize pages, such as news sites vs low-priority content?**

Assign each URL a priority based on signals like PageRank or in-link count, site authority, change frequency, and content type. The frontier is a priority queue, with separate queues for different priority bands and a scheduler that picks the highest-priority domain that is currently allowed by politeness. News sites can be given a freshness boost or a dedicated high-priority queue.

**Should you support re-crawling and how do you schedule that?**

Yes, otherwise results become stale. Estimate change frequency from sitemap lastmod timestamps, historical change rate, and content hash changes. Store an earliest_next_fetch timestamp per URL; a scheduler periodically scans for URLs whose time has passed and reinserts them into the frontier, with priority reflecting their importance and freshness.

## Worked example

Suppose a worker batch has two domains: news.example with crawl-delay 2 seconds and docs.example with no delay. At t=0 the frontier emits one URL from each. The fetcher for news.example records last_fetch=0 and increments domain concurrency. For docs.example it fetches immediately. The parser extracts `HTTP://Example.com:80/path?b=2&a=1#top`. Canonicalization yields `http://example.com/path?b=2&a=1` (lowercase scheme and host, default port removed, fragment removed, query order untouched). If that key is not in the visited store, the URL enters the frontier; if a Bloom filter says 'possibly seen', the store is checked and, if absent, it is admitted. news.example cannot be fetched again until t=2, while docs.example is available immediately. Later, a re-crawl scheduler reinserts URLs whose earliest_next_fetch has passed.

## Common traps

- Using a Bloom filter as the authoritative visited-set check, dropping new URLs when its false positives fire.
- Blindly sorting query parameters during canonicalization, which can merge URLs that are different resources on sites where parameter order or duplicate keys matter.
- Ignoring robots.txt or per-domain concurrency limits; a crawler that hits a domain too fast can be blocked or violate site policy.
- Designing only for the initial crawl and omitting re-crawl scheduling, so the index goes stale and has no mechanism to refresh.

</details>

---

## Output prediction (`output-prediction` · pick_one)

### 9. Indexes · Hard

*sql · gate confidence 0.9*

<sub>to object to this card: `## sql-indexes` then `match: A PostgreSQL table has a secondary index on (a, b, c). You r`</sub>

**Question**

A PostgreSQL table has a secondary index on (a, b, c). You run: UPDATE t SET d = 5 WHERE a = 1 AND b = 2 AND c = 3; The update changes only column d, which is not part of any index. The new tuple version fits on the same heap page as the old version. What happens to the secondary index on (a, b, c)?

**Options**

A. The index is updated with a new entry for the new tuple version.
B. The index is not updated because HOT optimization applies.
C. The index is updated only if the WHERE clause uses an index scan.
D. The index is dropped and recreated.

**Answer (the reader is graded on)**

- Correct: B. The index is not updated because HOT optimization applies.

**Why (right answer, wrong reason is wrong)**

→ **A. The new tuple version fits on the same heap page and no indexed column changed, so HOT redirects the old index entry to the new tuple.**
  B. The WHERE clause uses an equality condition on all indexed columns, so the index is not needed for the update.
  C. PostgreSQL always updates secondary indexes on UPDATE, regardless of which columns change.
  D. The index is on (a, b, c), and column d is not part of the index, so the index is automatically skipped.

**Reference answer**

The index is not updated. Because no indexed column changed and the new tuple version fits on the same heap page, PostgreSQL's HOT (Heap-Only Tuple) optimization applies. The old index entry is redirected to the new tuple via the line pointer, so the secondary index remains unchanged.

**Graded on**

- HOT avoids updating secondary indexes when no indexed column changes and the new tuple fits on the same page.
- Without HOT, PostgreSQL would add a new index entry for the new tuple version in every secondary index.
- The index on (a, b, c) is not affected because columns a, b, and c are unchanged.

<details><summary>The lesson this came from</summary>

An index is a separate data structure, usually a B-tree, that stores a sorted copy of one or more columns from a database table plus a pointer to the row the values came from. It lets the query planner seek or range-scan on key columns instead of scanning the entire table. Engines differ in clustering: SQL Server has one clustered index that determines physical row order and non-clustered indexes as separate B-trees; MySQL InnoDB always clusters by the primary key; PostgreSQL stores table rows in an unordered heap and all standard indexes are secondary.

## Why interviewers ask this

Interviewers use indexes to test whether you understand real database performance, not just syntax. They want to see you can choose a good index for a given query, reason about composite key order and covering indexes, and explain the write/storage tradeoff. Many candidates can recite CREATE INDEX but cannot predict when an index helps or hurts.

## The core idea

An index is a copy of data organized for search: it speeds up reads because the engine can walk a B-tree instead of scanning every row, but it adds storage and every insert/update/delete must keep the copies in sync. Composite indexes work left-to-right: equality columns position the seek, a range column bounds the scan, and later columns cannot narrow the seek range but can still be applied as predicates inside the index scan before row lookups in engines that support index condition pushdown. Write cost is engine-dependent: in PostgreSQL's append-only MVCC, an UPDATE creates a new tuple version and unless HOT optimization applies, all secondary indexes on the table receive entries for the new version, even when no indexed column changed.

## Key points

- Most general-purpose SQL indexes are B-trees that support O(log n + rows returned) seeks and range scans, compared with O(n) full table scans.
- A composite index on (a, b, c) can only be used efficiently for lookups that include leading columns; a query filtering only on b or c usually cannot use that index for a seek.
- For a WHERE clause with equality on a and range on b, c cannot narrow the seek range, but engines such as MySQL, SQL Server, PostgreSQL and Oracle can still apply c as an index filter while scanning the index.
- In SQL Server, clustered indexes define physical row order and are limited to one per table; MySQL InnoDB always has a clustered primary key; PostgreSQL has no clustered indexes and stores rows in a heap with secondary indexes pointing to row locations.
- In PostgreSQL's MVCC, an UPDATE writes a new tuple version and, unless HOT is possible on the same page, all secondary indexes are updated to point to the new version even if the updated columns are not part of any index.

## Your 60-second answer

A database index is a separate data structure, typically a B-tree, that keeps a sorted copy of one or more columns and pointers to the corresponding rows. It lets the optimizer find rows by seeking or scanning a small range instead of reading the whole table. In exchange, indexes consume storage and write operations must keep them in sync, so write-heavy tables can slow down significantly. How the columns are ordered matters: for a composite index, equality columns must come before range columns, and any column after the range cannot narrow the seek but can still be applied as a filter during the index scan in modern engines. Clustered indexes, where supported, define the table's physical order; non-clustered indexes are separate structures.

## If they dig deeper

**What are the main costs of creating too many indexes?**

Each index duplicates the key columns and adds storage. Writes must update indexes, increasing insert/update/delete latency. In MVCC engines like PostgreSQL, even updating a non-indexed column can force writes to every secondary index unless HOT optimization is possible on the same page.

**Given an index on (a, b, c) and WHERE a = 1 AND b > 2 AND c = 3, how much of the index is used?**

The B-tree can use a as an equality seek and then range scan b > 2. C cannot narrow the start or end of that b range because the index is sorted first by a, then b, so c values are not consecutive for all b > 2. Modern engines such as MySQL, SQL Server, PostgreSQL and Oracle still apply c as a residual predicate inside the index scan, avoiding base table lookups for rows that fail c = 3.

**Explain the difference between clustered and non-clustered indexes.**

A clustered index determines the physical order of table rows; SQL Server allows at most one per table and the leaf level is the data pages. MySQL InnoDB always stores rows in the primary key's clustered B-tree, with secondary indexes holding primary key values to find rows. PostgreSQL has no clustered index concept in its normal storage: rows live in an unordered heap, and every index, including the primary key, is a secondary structure pointing to row locations.

**Why does PostgreSQL update every secondary index when you change a non-indexed column?**

PostgreSQL uses MVCC: an UPDATE does not overwrite the old row, it writes a new physical tuple version. Every secondary index entry points to the physical tuple location, so the database must add entries for the new version into all indexes on the table. The HOT optimization avoids this only when the new tuple fits on the same heap page and no indexed column changes; then old index entries can be redirected via the line pointer, so secondary indexes remain unchanged.

## Worked example

Take an orders table with columns customer_id, order_date, status, and amount, and an index on (customer_id, order_date, status). A query asks: SELECT * FROM orders WHERE customer_id = 42 AND order_date BETWEEN '2024-01-01' AND '2024-06-30' AND status = 'shipped'. The B-tree descends to customer_id 42, then scans the order_date range as a contiguous block. Because the next key column status comes after order_date, it cannot start the scan at the first 'shipped' row inside that range; the scan visits all rows with order_date in that range. With index condition pushdown, the engine evaluates status = 'shipped' on the index entries and only performs base table lookups for rows that pass, avoiding I/O for rows that do not match. Without ICP, every row in the order_date range would trigger a lookup to check status.

## Common traps

- Believing an index on (a,b,c) can speed up a query that filters only on b or c; without leading column a, the B-tree cannot provide a direct seek.
- Over-indexing because each index helps a read; on a write-heavy table, the accumulated index maintenance can dominate and even hurt overall workload.
- Assuming 'c' is useless after a range on 'b' in a composite index; it cannot narrow the seek range but can still be used as an index filter before table access.
- Confusing clustered with unique: a clustered index concerns physical storage order, while a unique index is a constraint that rejects duplicate key values.

</details>

---

### 10. 1-D Dynamic Programming · Medium

*dsa · gate confidence 0.9*

<sub>to object to this card: `## 1-d-dynamic-programming` then `match: Consider the House Robber problem with nums = [2, 7, 9, 3, 1`</sub>

**Question**

Consider the House Robber problem with nums = [2, 7, 9, 3, 1]. What is the maximum amount of money that can be robbed, assuming you cannot rob two adjacent houses?

**Options**

A. 11
B. 12
C. 15
D. 19

**Answer (the reader is graded on)**

- Correct: B. 12

**Reference answer**

The maximum amount is 12. Using the recurrence dp[i] = max(dp[i-1], dp[i-2] + nums[i-1]) with dp[0]=0 and dp[1]=nums[0]=2, we get dp[2]=max(2,0+7)=7, dp[3]=max(7,2+9)=11, dp[4]=max(11,7+3)=11, dp[5]=max(11,11+1)=12. The optimal choice is to rob houses 1 and 3 (2+9=11) or houses 2 and 5 (7+1=8), but the best is 2+9+1=12 by robbing houses 1, 3, and 5.

**Graded on**

- The recurrence is dp[i] = max(dp[i-1], dp[i-2] + nums[i-1]).
- Base cases are dp[0]=0 and dp[1]=nums[0].
- The maximum amount for this input is 12.

<details><summary>The lesson this came from</summary>

1-D dynamic programming is an algorithmic technique that solves a problem by defining a single state variable, usually an index, and storing the answer for each subproblem in an array dp. Each entry dp[i] is computed from earlier entries via a recurrence, implemented either top-down with memoization or bottom-up with iteration. This avoids recomputing overlapping subproblems when the problem has optimal substructure. It appears in counting, optimization, and feasibility problems on linear sequences, strings, and simple coin/knapsack choices.

## Why interviewers ask this

Interviewers use these problems to test whether you can recognize that a brute-force recursive solution contains overlapping subproblems and can replace it with a cache or table. They also probe your ability to derive an exact recurrence from problem constraints and implement it without off-by-one errors. Common 1-D DP questions such as Climbing Stairs, House Robber, Coin Change, Word Break, and Decode Ways show up across many companies, and the interviewer may follow up by changing one condition.

## The core idea

The central skill in 1-D DP is identifying a recurrence over a single index. Once you can write dp[i] in terms of earlier dp values, the implementation is just a loop that fills an array from base cases upward. The array entry stores the answer to a subproblem, not a partial guess. For example, in House Robber each dp[i] stores the best robbery value considering the first i houses, and the recurrence is dp[i] = max(dp[i-1], dp[i-2] + nums[i-1]) with base cases dp[0]=0 and dp[1]=nums[0]. Many 1-D DP solutions can be compressed to O(1) space when only a fixed number of previous states are needed. The hard part is not writing the loop but formulating the state and transition correctly.

## Key points

- 1-D DP is applicable when a problem has overlapping subproblems and optimal substructure, and the subproblem can be indexed by one variable.
- Climbing Stairs has recurrence dp[i] = dp[i-1] + dp[i-2] with base cases dp[0] = 1 and dp[1] = 1 for the number of ways to reach step i.
- House Robber has recurrence dp[i] = max(dp[i-1], dp[i-2] + nums[i-1]) for the first i houses, with dp[0] = 0 and dp[1] = nums[0].
- Coin Change uses dp[amount] = min(dp[amount - coin] + 1) over all coins, with dp[0] = 0; Word Break uses dp[i] as whether the prefix s[0:i] can be segmented into dictionary words.
- Maximum Product Subarray must track both maximum and minimum product because a negative number can turn a minimum into a maximum.

## Your 60-second answer

One-dimensional dynamic programming means defining an array dp where each entry stores the answer for a subproblem at one index, then filling that array with a recurrence. It works when subproblems overlap and the solution has optimal substructure, so the same subproblem would otherwise be recomputed many times. For example, Climbing Stairs uses dp[i] = dp[i-1] + dp[i-2], and House Robber uses dp[i] = max(dp[i-1], dp[i-2] + nums[i-1]). The key trade-off is memory: although a full table is easy to reason about, many 1-D DP recurrences only need the last one or two values, so you can often reduce O(n) space to O(1). The real interview skill is formulating the state and transition correctly, not just looping.

## If they dig deeper

**How do you recognize that a problem should be solved with DP?**

Check whether the problem has optimal substructure and overlapping subproblems: a solution can be constructed from optimal solutions to smaller subproblems, and those smaller subproblems repeat. If a naive recursion revisits the same inputs many times, memoization or bottom-up DP will help. In 1-D DP the subproblems are ordered by a single index.

**When would you prefer top-down memoization over bottom-up tabulation?**

Top-down is often easier to write when the valid transitions are not a simple left-to-right order or when many states are never reached. Bottom-up is usually faster by avoiding recursion overhead and makes constant-space optimization possible when only a few previous states matter. I would default to bottom-up for linear 1-D problems after deriving the recurrence.

**Can you reduce the House Robber solution to O(1) space? How?**

Yes. The recurrence depends only on dp[i-1] and dp[i-2], so keep two variables: prev1 for dp[i-1] and prev2 for dp[i-2]. At each house value val, compute current = max(prev1, prev2 + val), then shift prev2 = prev1 and prev1 = current. Climbing Stairs uses the same two-variable trick.

**Why do you need a minimum product in Maximum Product Subarray?**

Because multiplying two negative numbers yields a positive product. If the current number is negative, the maximum product ending here may come from the minimum product ending at the previous index. So at each index we track both max_prod and min_prod, swap them when nums[i] is negative, and update both.

**How does the O(n log n) Longest Increasing Subsequence algorithm work?**

It uses patience sorting with a tails array. For each number, binary search the first element in tails that is greater than or equal to it and replace it; if none exists, append it. The length of tails is the LIS length. This computes only the length, not the actual subsequence.

## Worked example

Take nums = [1,2,3,1] for House Robber. Define dp[i] as the maximum money from the first i houses, with dp[0] = 0 and dp[1] = nums[0] = 1. For dp[2], either skip the second house and keep dp[1] = 1, or rob it and add dp[0] = 0 plus 2, giving 2, so dp[2] = 2. For dp[3], skipping gives dp[2] = 2; robbing house 3 adds 3 to dp[1] = 1, total 4, so dp[3] = 4. For dp[4], skipping gives dp[3] = 4; robbing house 4 adds 1 to dp[2] = 2, total 3, so dp[4] = 4. The maximum amount is 4.

## Common traps

- Solving every maximization problem with DP even when there are no overlapping subproblems; a greedy approach may be correct and faster.
- Mixing 0-based and 1-based indexing in House Robber or Climbing Stairs, causing off-by-one errors in nums[i-1] versus nums[i].
- For Maximum Product Subarray, tracking only the largest product and not the smallest, which fails on arrays with negative numbers.
- Skipping base cases like n=1 or amount=0, leading to index-out-of-range or returning an uninitialized sentinel in Coin Change.

</details>

---

## Counter-example (`counter-example` · pick_one)

### 11. Collections Framework · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-collections-framework` then `match: Which of the following statements about the Java Collections Framework is false?`</sub>

**Question**

Which of the following statements about the Java Collections Framework is false?

**Options**

A. Map extends Collection.
B. HashMap iteration order is insertion order.
C. PriorityQueue guarantees sorted iteration order.
D. Collections.unmodifiableList returns a deep immutable copy.

**Answer (the reader is graded on)**

- Correct: B. HashMap iteration order is insertion order.

**Reference answer**

HashMap does not guarantee any iteration order. Its iteration order depends on hash distribution and capacity, not insertion order or sorted order. LinkedHashMap preserves insertion order, and TreeMap sorts keys.

**Graded on**

- HashMap makes no order guarantee.
- LinkedHashMap preserves insertion order.
- TreeMap sorts keys in natural or comparator order.

<details><summary>The lesson this came from</summary>

The Java Collections Framework is the set of interfaces, implementations, and algorithms in java.util for representing and manipulating groups of objects as a single unit. Its core interfaces are Collection (extending Iterable) with subinterfaces List, Set, Queue, and Deque; Map is part of the framework but does not extend Collection. Concrete classes include ArrayList, LinkedList, HashSet, TreeSet, PriorityQueue, HashMap, TreeMap, and concurrent variants. The Collections utility class provides static methods such as sort, binarySearch, shuffle, and unmodifiable views.

## Why interviewers ask this

Interviewers use Collections questions to test whether you know which data structure to choose under real constraints: ordering, duplicates, null handling, thread safety, and time complexity. They also probe whether you understand the difference between interface contracts and implementation guarantees, because that is what prevents production bugs. The framework is so central to Java code that weak answers here signal weak practical Java.

## The core idea

The framework separates contracts from implementations: program to List, Set, or Map rather than to ArrayList or HashMap, so you can swap implementations. The four main data structure shapes are ordered sequences with index access (List), unique unordered or sorted elements (Set), key-value mappings (Map), and FIFO/priority task queues (Queue/Deque). Each implementation has a specific backing structure: ArrayList is a resizable array, LinkedList is a doubly-linked list, HashSet is a hash table, TreeSet is a red-black tree. Choosing a collection means matching expected operations to these underlying structures: O(1) get by index for ArrayList versus O(1) insertion at ends for LinkedList. The Collections utility class supplies polymorphic algorithms that operate on these interfaces, such as sort and binarySearch.

## Key points

- The Collection interface extends Iterable and is the root of List, Set, Queue, and Deque; Map is part of the Collections Framework but does not extend Collection.
- ArrayList is a resizable array with O(1) get/set by index and amortized O(1) add at the end, while LinkedList is a doubly-linked list with O(1) add/remove at either end.
- HashSet and HashMap provide average O(1) contains/get/put with good hash distribution but no iteration-order guarantee; LinkedHashSet and LinkedHashMap preserve insertion order.
- TreeSet and TreeMap store elements in sorted order in a red-black tree, giving O(log n) operations; a comparator or natural ordering defines the order.
- Collections is a utility class of static methods such as sort (for lists), binarySearch, shuffle, reverse, and unmodifiableList.

## Your 60-second answer

The Java Collections Framework is the set of interfaces, implementations, and algorithms in java.util for storing and manipulating groups of objects. The core interfaces are Collection, with subinterfaces List, Set, Queue, and Deque, plus Map, which is part of the framework but does not extend Collection. List gives ordered, index-based access; Set enforces uniqueness; Map stores key-value pairs; Queue handles FIFO or priority access. Choosing the right implementation depends on your operation pattern: ArrayList is a resizable array with O(1) get by index, LinkedList is a doubly-linked list with O(1) insertion at the ends, HashSet gives average O(1) contains without order, and TreeSet gives sorted order at O(log n). One trade-off is that ArrayList's fast random access costs O(n) insertion or removal in the middle, so a LinkedList may be better for frequent additions at the head or tail.

## If they dig deeper

**What is the difference between Collection and Collections?**

Collection is the root interface of most collection types, extended by List, Set, and Queue. Collections is a utility class in java.util containing static methods such as sort, binarySearch, shuffle, and unmodifiableList that operate on Collection instances. Mixing them up is a common interview slip.

**How do ArrayList and LinkedList differ in performance and when should you use each?**

ArrayList is backed by a dynamic array, so get and set by index are O(1), but inserting or removing in the middle is O(n) because elements shift. LinkedList is a doubly-linked list, so get by index is O(n), but inserting or removing at either end is O(1) and removal of a known node is O(1). Use ArrayList for random access and typical iteration, and LinkedList for frequent add/remove at the ends, like a queue or deque.

**Why is HashMap not ordered and what do LinkedHashMap and TreeMap do differently?**

HashMap spreads entries across buckets using the key's hash code, so iteration order depends on hash distribution and capacity, not insertion or sort order. LinkedHashMap maintains a doubly-linked list through entries to preserve insertion order (or access order if configured). TreeMap stores entries in a red-black tree sorted by natural key order or a comparator, giving O(log n) operations and sorted views.

**What does Collections.unmodifiableList return and can the original list still change?**

unmodifiableList returns a read-only view backed by the original list; any mutating method on the view throws UnsupportedOperationException. Changes to the underlying list are still visible through the unmodifiable view, so it is not a deep immutable copy. To prevent external mutation, do not retain a reference to the backing list.

**How is PriorityQueue different from a sorted list, and is it thread-safe?**

PriorityQueue is a heap-based queue where the head is always the least element according to natural order or a supplied comparator, but the rest of the elements are not necessarily sorted; add and poll are O(log n) and peek is O(1). Unlike a TreeSet, it allows duplicates and does not store all elements in sorted order. It is not thread-safe; use PriorityBlockingQueue for concurrent access.

## Worked example

Given an ArrayList<Integer> with five elements [10,20,30,40,50], inserting 15 at index 1 shifts elements 20 through 50 one position right, which is O(n) because all trailing elements move. A LinkedList<Integer> with the same five elements inserts at index 1 by adjusting two node references, but to reach index 1 it must traverse from the head, making add(index, element) O(n) as well. The LinkedList's O(1) insertion advantage only applies at the ends using addFirst/addLast or with an iterator at the insertion point. For a PriorityQueue<Integer> with [5,1,3], peek returns 1, the least element; after poll, the heap internally adjusts and peek returns 3.

## Common traps

- Saying Map extends Collection; Map is part of the framework but is a separate interface hierarchy, so methods like add or iterator do not apply.
- Claiming HashMap iteration order is insertion or sorted; HashMap makes no order guarantee, while LinkedHashMap preserves insertion order and TreeMap sorts keys.
- Assuming unmodifiable views are deeply immutable copies; they are backed by the original collection and reflect later changes to it.
- Using PriorityQueue for sorted iteration; it only guarantees the head is the least element, and iterating with its Iterator may yield elements in no particular order.

</details>

---

### 12. Lambda expressions · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-lambda-expressions` then `match: Which of the following lambda expressions fails to compile w`</sub>

**Question**

Which of the following lambda expressions fails to compile when assigned to the declared functional interface type?

**Options**

A. Runnable r = () -> System.out.println("hi");
B. Predicate<String> p = s -> s.isEmpty();
C. Consumer<String> c = s -> s.length();
D. Function<String, Integer> f = s -> s.length();

**Answer (the reader is graded on)**

- Correct: C. Consumer<String> c = s -> s.length();

**Reference answer**

`Consumer<String> c = s -> s.length();` fails because Consumer's `accept` method returns void, but the expression body `s.length()` returns an int. A lambda body that is an expression must be compatible with the target method's return type; an int cannot be returned where void is expected.

**Graded on**

- A lambda expression body must be compatible with the target functional interface's single abstract method return type.
- Consumer<T> has method void accept(T), so an expression body returning a value is invalid.
- The other options match their target interfaces: Runnable takes no arguments and returns void, Predicate returns boolean, and Function returns a value.

<details><summary>The lesson this came from</summary>

A lambda expression is a syntactic construct that creates an instance of a functional interface by supplying the body of its single abstract method inline. The arrow operator separates an optional parameter list from a body, which can be a single expression or a block. Lambda expressions were introduced in Java 8 as a concise alternative to anonymous classes that implement exactly one method.

## Why interviewers ask this

Interviewers ask about lambdas to check whether you understand Java 8's shift toward passing behavior as data and how lambdas relate to functional interfaces. They probe target typing, capture rules, and the common java.util.function interfaces because those feed directly into streams and collection pipelines.

## The core idea

In Java, a lambda expression is the body of the one abstract method in a target functional interface. The compiler uses the expected type from the assignment, cast, or method argument to infer parameter types and check return compatibility. A lambda can capture local variables only if they are effectively final—never reassigned anywhere in their scope—but it can always read and modify instance fields and static fields. At runtime, the JVM uses invokedynamic and the LambdaMetafactory to create the call site rather than generating a separate anonymous class file at compile time. A lambda body may be a single expression whose value is returned automatically, or a block with explicit returns and statements.

## Key points

- A lambda expression always implements a functional interface, which has exactly one abstract method; default and static methods do not count toward that one.
- Target typing determines the lambda's type from the surrounding context—assignment, cast, or method argument—not from the lambda's own body.
- Parameter types may be omitted, a single untyped parameter may drop parentheses, and the body can be an expression returning a value or a block with statements and explicit returns.
- Captured local variables must be effectively final, meaning they are never reassigned anywhere in their scope, while instance fields and static variables may be read and modified freely.
- Common functional interfaces include Predicate<T> with boolean test(T), Function<T,R> with R apply(T), Consumer<T> with void accept(T), and Supplier<T> with T get().

## Your 60-second answer

A lambda expression is Java's concise syntax for implementing a functional interface inline. You write the parameter list, an arrow, and a body, and the compiler treats that as providing the single abstract method of whatever functional interface is expected at that spot. For example, `Runnable r = () -> System.out.println(42);` creates a Runnable without the boilerplate of an anonymous class. Lambdas matter because they let you pass behavior as data to methods like `forEach`, `filter`, and `map`, especially with the Streams API added in Java 8. One trade-off is that they can only target interfaces with exactly one abstract method, so if you need to implement two methods you still write an anonymous class. Another trade-off is captured local variables must be effectively final, which sometimes forces a workaround like using a single-element array or a field.

## If they dig deeper

**What is a functional interface, and how does @FunctionalInterface work?**

A functional interface is an interface with exactly one abstract method. Default and static methods do not count toward that one. The @FunctionalInterface annotation is optional but when present it makes the compiler fail if the interface has zero or more than one abstract method.

**Can you assign a lambda to Object or use var with it? Why not?**

No. A lambda expression needs a target type that is a functional interface because it supplies the body of that interface's single abstract method. Object has no abstract method, so the compiler cannot infer a functional interface; you need a cast like `(Runnable) () -> ...` or an explicit functional interface target such as a variable declaration.

**What are the rules for capturing variables in a lambda expression?**

Local variables and parameters from the enclosing method can be read only if they are effectively final—never reassigned anywhere in their scope. Instance fields and static fields can always be read and modified. A lambda cannot access default methods of the functional interface it implements because there is no interface instance `this` available inside the lambda.

**How does the JVM implement lambdas differently from anonymous inner classes?**

At compile time, the compiler emits an invokedynamic call site with a method handle to a synthetic private method containing the lambda body. At runtime, the LambdaMetafactory uses that method handle to generate or return a class implementing the functional interface; no separate class file is created for each lambda, unlike anonymous inner classes which generate a distinct class at compile time.

**What are the scoping differences between a lambda and an anonymous inner class?**

A lambda is lexically scoped: `this` and `super` refer to the enclosing instance, not the lambda object, and a lambda parameter cannot shadow a local variable from the enclosing method. An anonymous inner class has its own `this`, and its parameters and locals can shadow enclosing variables because it introduces a new nested scope.

## Worked example

Take `List<String> words = Arrays.asList("apple", "pear", "kiwi");` and the call `Collections.sort(words, (a, b) -> a.length() - b.length());`. The second argument's expected type is `Comparator<String>`, whose `compare` method takes two `String` parameters and returns `int`, so the compiler infers `a` and `b` as `String` and accepts the expression body as the returned difference. If you tried to assign that same lambda to a `Function<String, Integer>`—a one-parameter interface—the parameter count mismatches and compilation fails even though an int is returned. For capturing, `int limit = 5; List<Integer> xs = Arrays.asList(1, 2, 3); xs.replaceAll(x -> x * limit);` compiles because `limit` is never reassigned; adding `limit = 6` anywhere in the method makes `limit` not effectively final and the lambda will not compile. These two examples show target typing and effective final capture.

## Common traps

- Assigning a lambda to Object or using var without a functional interface target: compilation fails because a lambda has no independent type.
- Thinking a captured local variable can be reassigned as long as the reassignment happens before the lambda: any reassignment in scope breaks effective finality, even before the lambda is created.
- Conflating lambda with anonymous inner class for `this`: inside a lambda `this` is the enclosing object, not the lambda instance.
- Using a zero-argument lambda as a Consumer: Consumer's accept method takes one argument, so `() -> list.add(x)` targets a zero-argument void interface such as Runnable, not Consumer.

</details>

---

## Trace the value (`trace-the-value` · numeric)

### 13. Sliding Window · Medium

*dsa · gate confidence 0.9*

<sub>to object to this card: `## sliding-window` then `match: You are given an array of n integers and a fixed window size`</sub>

**Question**

You are given an array of n integers and a fixed window size k. You need to compute the maximum value in every contiguous subarray of length k using a monotonic deque. What is the total number of times elements are removed from the back of the deque over the entire algorithm, in the worst case?

**Answer (the reader is graded on)**

- 0.0 ± 0.0

**Reference answer**

Each element is removed from the back of the deque at most once, because once removed it never re-enters the deque. Therefore the total number of back-removals across the whole algorithm is at most n.

**Graded on**

- Each element is pushed onto the deque exactly once when right passes over it.
- An element removed from the back is never pushed again, so it can be removed at most once.
- The total number of back-removals is bounded by the number of pushes, which is n.

<details><summary>The lesson this came from</summary>

The sliding window technique maintains a contiguous range [left, right] over an array or string. A loop extends right to add elements and, when a constraint is violated, moves left to remove elements; result state is updated incrementally. Fixed-size windows of size k slide by adding the element at right and removing at right-k. Variable-size windows use a condition-specific rule to shrink. For maximum or minimum values inside each window, a monotonic deque replaces a heap and gives O(1) amortized per element.

## Why interviewers ask this

Interviewers use it to see whether you can avoid recomputing every subarray from scratch, because problems such as Minimum Window Substring at Lyft, Snap, and Snowflake or Sliding Window Maximum at Citadel and Zepto become much slower with naive scanning. They also test whether you can maintain the right state—counts, sums, or deque invariants—that updates in O(1) when a pointer moves.

## The core idea

The key reason a sliding window is linear is that left and right both only advance. Each element enters the window when right passes over it and leaves when left passes over it, so there are at most 2n pointer moves. The entire algorithm depends on maintaining state that supports add, remove, and query of the target property in constant time. For variable-size windows, a common loop expands until the window becomes valid, then shrinks from the left to find the smallest windows or to restore validity after a violation. For window maximum problems, the state is a monotonic deque of indices; smaller elements are removed from the back because they can never become the maximum while a larger element is still in the window.

## Key points

- Both pointers move only forward, so each element is added and removed at most once, giving amortized O(n) time with O(1) state updates.
- Variable-size windows expand until a constraint is violated, then shrink from the left until the constraint is satisfied again, recording the best valid window.
- For a fixed window of size k, use a monotonic deque of indices sorted by value decreasing, so the front is the maximum for the current window.
- Character-frequency windows need counts, not sets, because duplicates matter in problems like Permutation in String and Minimum Window Substring.
- Sliding window applies to contiguous subarrays and substrings; it does not solve subsequence problems and requires a monotonic feasibility condition.

## Your 60-second answer

A sliding window keeps two pointers, left and right, over the input and moves them in one direction over a contiguous range. For a fixed window of size k, you add the new element when right advances and remove the element k positions behind it. For a variable window, you typically expand right until the window satisfies a constraint, then move left while it still does, or until it becomes valid again after a violation, recording the best answer along the way. Because each element enters and leaves at most once, the whole scan is O(n) as long as updating the state is O(1). The real design question is the state: a sum for a fixed numeric window, a frequency map for character constraints, or a monotonic deque when you need the maximum or minimum of each window. It only applies to contiguous subarrays or substrings.

## If they dig deeper

**When would you choose a fixed-size window instead of a variable-size window?**

Use a fixed window when the problem gives the subarray length k, such as maximum sum of k consecutive elements or maximum of each k-size window. Use a variable window when the length is unknown and the goal is to optimize length while satisfying a condition, such as longest substring or minimum window substring.

**Walk through Longest Substring Without Repeating Characters on "abcabcbb".**

Maintain a set or last-index map of characters in the current window. Right advances and adds characters; when a duplicate appears, move left forward, removing characters until the duplicate is gone. For "abcabcbb", the valid windows peak at "abc", then "bca", then "cab", all of length 3, and later duplicates prevent anything longer.

**Why is the total complexity O(n) despite the inner while loop that shrinks the window?**

The inner while loop moves left forward, and left never moves backward. Over the whole execution, left can move at most n positions, so the shrink work is bounded by n. Combined with right moving n positions, total work is O(n), not O(n^2).

**How does a monotonic deque solve Sliding Window Maximum in O(n)?**

The deque stores indices in decreasing order of values. Before adding a new element, remove indices from the back whose values are smaller or equal, because they can never be maximum while the new larger element is in the window. Remove expired indices from the front when they fall outside the current k-size window, and the front is the current maximum.

**What state and validity check would you use for Minimum Window Substring with duplicate characters in t?**

Keep a frequency map or array for characters in t, a matching map for the current window, and a counter of how many required characters are satisfied. Expand right; when a character reaches its target count, increment satisfied. When satisfied equals the number of distinct characters in t, shrink from the left while the window is still valid, updating the shortest valid window before removing a needed character.

## Worked example

For s = "ADOBECODEBANC" and t = "ABC", expand right until index 5; the window [0,5] = "ADOBEC" contains A, B, and C, so record length 6. Removing A at index 0 loses the only A, so left moves to 1 and the window is invalid. Expand right until index 10, where A appears again. The window [1,10] is valid; remove D at 1, O at 2, B at 3, and E at 4 while still valid, but C at index 5 is the only C, so left stops at 5. Continue to index 12, where the second C appears. Now shrink from index 5: remove C, O, D, and E from indices 5 through 8, leaving [9,12] = "BANC". Removing B at index 9 would lose the only B, so the minimum length is 4 and the answer is "BANC".

## Common traps

- Nested loop scanning every subarray from scratch is O(n^2) and often times out for n = 10^5, which is where sliding window is expected.
- Forgetting to shrink an invalid variable-size window leaves the left pointer behind and reports invalid or oversized windows.
- Using a set instead of a frequency map for problems with duplicate characters corrupts counts in Minimum Window Substring or Permutation in String.
- Applying variable-size two-pointer sliding window to non-monotonic conditions such as subarray sum equals k with negative numbers, because shrinking can miss valid windows.

</details>

---

### 14. Garbage Collection · Medium

*java · gate confidence 0.9*

<sub>to object to this card: `## java-garbage-collection` then `match: A HotSpot young collection in Serial GC copies live objects `</sub>

**Question**

A HotSpot young collection in Serial GC copies live objects from Eden and one survivor space into the other survivor space. Suppose Eden is 8 MB, each survivor space is 1 MB, and at the moment of collection Eden contains 7 MB of garbage and 1 MB of live objects, while the source survivor space contains 0.5 MB of live objects. How many megabytes of memory are reclaimed (made available for new allocations) by this young collection?

**Answer (the reader is graded on)**

- 7.5 ± 0.1

**Reference answer**

The young collection reclaims 7.5 MB. Eden's 7 MB of garbage is reclaimed because the entire Eden space is reset after live objects are copied out, and the source survivor space's 0.5 MB of garbage is reclaimed because that space is also cleared after its live objects are copied to the destination survivor space. The live objects (1 MB from Eden and 0.5 MB from survivor) are copied to the destination survivor space, so they are not reclaimed.

**Graded on**

- Young collections in Serial GC are copying collectors: live objects are copied out of Eden and the source survivor space, then both spaces are reset.
- All garbage in Eden and the source survivor space is reclaimed, regardless of individual object sizes.
- Live objects are copied to the destination survivor space and are not reclaimed.

<details><summary>The lesson this came from</summary>

Java's HotSpot JVM manages heap memory automatically by periodically finding objects that are unreachable from GC roots and reclaiming their memory. The heap is generational: most new objects are allocated in Eden and a young collection copies the few survivors to a survivor space, while longer-lived objects are promoted to the old generation. Since Java 8 class metadata lives in Metaspace instead of Permanent Generation. Different HotSpot collectors—Serial, Parallel, G1, ZGC, Shenandoah—trade off pause time, throughput, and footprint.

## Why interviewers ask this

Interviewers use this to test whether you understand automatic memory management, reachability, and the generational hypothesis, not just the phrase 'mark and sweep'. They also probe whether you can choose a collector for a workload and avoid myths like System.gc() forcing collection or finalize() being reliable.

## The core idea

GC reclaims only objects unreachable from roots such as thread stacks, static fields, and JNI references. Most objects die young, so HotSpot uses a copying collector in the young generation: it copies live objects out of Eden into a survivor space and then resets Eden, which is cheap when most objects are garbage. Survivors are copied between survivor spaces and eventually promoted to the old generation. The old generation is collected less often, historically by mark-sweep-compact; G1 instead divides the heap into regions and evacuates live objects from the regions with the most reclaimable space. The key trade-off is stop-the-world pause time versus throughput.

## Key points

- HotSpot uses a generational heap: new objects allocate in Eden, surviving objects are copied between two survivor spaces, and after enough young collections they are promoted to the old generation.
- Young collections in Serial, Parallel, and G1 are copying/evacuating collectors, not mark-and-sweep: live objects are copied and the entire source space is reused.
- Since Java 9, G1 is the default HotSpot collector; before Java 9 the server-class default was Parallel GC.
- System.gc() and Runtime.gc() only request collection and never guarantee that a GC will run.
- Strong, soft, weak, and phantom references define different reachability strengths; finalize() is deprecated for removal and Cleaner (Java 9+) is the recommended replacement.

## Your 60-second answer

Java garbage collection identifies objects that are no longer reachable from GC roots—such as thread stacks, static fields, and JNI handles—and reclaims them automatically. HotSpot uses a generational heap: new objects allocate in Eden, and when Eden fills, a young collection copies the few live objects into a survivor space and resets Eden instead of sweeping every dead object. Objects that survive enough young collections are promoted to the old generation. The old generation is collected less often, historically with mark-sweep-compact, while modern G1 evacuates live objects out of selected regions. Since Java 9, G1 is the default HotSpot collector; before that, Parallel GC was the typical server default. The main trade-off is pause time versus throughput: concurrent collectors reduce pauses but consume more CPU, while parallel stop-the-world collectors maximize throughput but pause application threads.

## If they dig deeper

**What counts as a GC root in Java?**

Thread stacks, static fields, JNI references, and internal JVM structures such as class metadata and synchronization monitors. Any object reachable by following references from these roots is considered live; unreachable objects are eligible for collection.

**Why is the heap divided into young and old generations?**

Most Java objects die shortly after allocation, so collecting only the young generation frequently is very cheap with a copying collector. Long-lived objects are promoted and collected less often, which reduces total work and pause time compared with scanning the whole heap every time.

**How does Serial GC differ from Parallel GC?**

Serial uses one thread for stop-the-world collections and is intended for small heaps or single-processor environments. Parallel uses multiple threads to speed up stop-the-world collections for better throughput on multi-core machines; both still pause all application threads.

**How does G1 differ from the old CMS collector?**

G1 divides the heap into fixed-size regions and collects the subset with the most reclaimable garbage, evacuating live objects and returning empty regions to the heap. CMS ran most of its marking concurrently but was prone to fragmentation and concurrent mode failure; it was deprecated in Java 9 and removed in Java 14.

**For a low-latency service with a 64 GB heap, which collector would you evaluate and how would you tune it?**

Start with G1 and set a pause-time target such as -XX:MaxGCPauseMillis=50 or lower, and keep -Xms equal to -Xmx to avoid heap resizing pauses. If pauses still miss the latency budget, evaluate ZGC or Shenandoah, which are concurrent compacting collectors that aim to keep pauses in the low milliseconds regardless of heap size, then measure with GC logs and adjust region sizes or tenuring threshold only when the data supports it.

## Worked example

Take a loop that allocates 1,000 short-lived 1 KB byte arrays per iteration and keeps only the most recent one in a field. After many iterations, Eden fills. At the next young collection, the collector scans the GC roots, finds the single referenced array and any other live objects, copies those few kilobytes into survivor space, and resets the entire Eden. The other 999 dead arrays are not swept individually; their memory is reclaimed because Eden is cleared. If the same array survives enough young collections, the copying collector promotes it to the old generation. Later, when the old generation fills, G1 selects the regions with the most garbage, evacuates the live objects from those regions into other regions, and recycles the now-empty regions without walking every dead object.

## Common traps

- Claiming all Java garbage collection is mark-and-sweep; young collections and G1 are primarily copying/evacuating collectors, so dead objects are not swept individually.
- Believing System.gc() or Runtime.gc() guarantees immediate collection; the JVM may ignore the hint entirely or run collection much later.
- Using finalize() for resource cleanup; it is deprecated for removal, unpredictable in timing, and can resurrect objects or delay GC.
- Treating soft references as reliable cache entries that stay until OutOfMemoryError; the collector may clear them earlier under memory pressure, so the cache can be empty at any GC.

</details>

---

## Failure diagnosis (`failure-diagnosis` · pick_one)

### 15. Design a chat system · Medium

*system_design · gate confidence 0.85*

<sub>to object to this card: `## sd-design-a-chat-system` then `match: A gateway server crashes while holding active WebSocket conn`</sub>

**Question**

A gateway server crashes while holding active WebSocket connections for several users. Which of the following is the most likely immediate consequence for message delivery to those users, assuming the system follows the design described?

**Options**

A. Messages are lost permanently because the gateway held the only copy of the socket state.
B. Messages are queued in the database and delivered automatically when the user reconnects, without any push notification.
C. The chat service retries delivery to the dead gateway until it comes back online, causing indefinite delays.
D. Messages are delivered via push notification, and the client backfills missed messages after reconnecting.

**Answer (the reader is graded on)**

- Correct: D. Messages are delivered via push notification, and the client backfills missed messages after reconnecting.

**Reference answer**

Messages sent to those users will be treated as undeliverable over WebSocket and fall back to push notifications until the clients reconnect and re-register with a new gateway. The central registry entry for the dead gateway becomes stale, so the chat service cannot route to an active socket and must rely on the offline path.

**Graded on**

- A crashed gateway leaves stale registry entries mapping users to a dead host.
- The chat service cannot deliver over WebSocket and falls back to push notifications.
- Clients detect the broken connection and reconnect to another gateway, which overwrites the registry entry.
- Missed messages are backfilled using per-conversation sequence numbers after reconnection.

<details><summary>The lesson this came from</summary>

A chat system maintains persistent WebSocket connections from each online client to one of several horizontally scaled gateway servers. A central registry in Redis or etcd maps each user ID to the gateway host that currently holds their active connection. Messages are stored durably in a database and then delivered over those WebSockets; offline users receive push notifications through FCM or APNs, whose payloads can carry standard text messages. Group chats fan out the same stored message to all members, often through internal queues or pub/sub.

## Why interviewers ask this

This question tests whether you can design a stateful, bidirectional system rather than a request-response API. The interviewer is probing your handling of connection state, presence, message ordering, delivery acknowledgements, and fan-out under scale. A strong answer separates the connection layer from the message service and shows how the system recovers when a gateway fails.

## The core idea

The core is decoupling connection state from message processing. Clients connect to any gateway behind a load balancer; that gateway registers the user in a central lookup table. When a message is sent, the chat service persists it first, then consults the registry to find the recipient's gateway and forwards the payload for socket delivery. Offline delivery falls back to push, and modern APNs/FCM payloads are large enough to include the message text instead of only a wake-up signal. For groups, the chat service fans out to each member's gateway, using queues or per-group pub/sub to smooth large bursts.

## Key points

- Gateways are horizontally scaled behind a load balancer; a central registry such as Redis or etcd maps user ID to the arbitrary gateway host currently holding the connection.
- Messages are persisted in a database keyed by conversation/channel before delivery; delivery over active WebSockets is separate from push fallback for offline users.
- APNs and FCM push payloads support up to 4 KB, so standard text messages can be delivered directly in the notification rather than requiring an immediate app sync.
- Group fan-out should not assume one server per group; use per-group pub/sub or queues so gateway nodes deliver to only their local members.
- Delivery semantics require client acknowledgements: sent means stored, delivered means the client acked receipt, read means the user opened the conversation.

## Your 60-second answer

A chat system has three main pieces: WebSocket gateway servers, a presence service, and a chat service that persists and fans out messages. Clients connect to a gateway behind a load balancer; the gateway registers the user ID in a central registry like Redis. When Alice sends a message to Bob, the chat service stores it in the messages table, looks up Bob's active gateway, and tells that gateway to push the message over Bob's socket. If Bob is offline, the chat service enqueues a push notification, and FCM or APNs delivers it; modern payloads can carry the text directly. For group chats, the service fans out to every member, using queues or pub/sub for large groups. The main trade-off is that WebSockets give low latency but make the connection layer stateful, so you need heartbeat detection and re-registration when a gateway fails.

## If they dig deeper

**After a client connects, how does the system route a message to that client?**

The gateway writes a mapping from the user's ID to its own host in a central registry such as Redis or etcd. The chat service looks up the recipient's ID at send time and forwards the message to that gateway host. When the connection drops, the gateway removes or expires the mapping.

**What happens if a gateway server dies with active connections?**

Clients detect the broken connection and reconnect through the load balancer to another gateway. The new gateway overwrites the registry entry, and the client fetches missed messages using a per-conversation sequence number or timestamp. Gateway heartbeats let other components stop routing to the dead host quickly.

**How do you ensure messages arrive in order?**

Assign each message a monotonically increasing sequence number per conversation at the chat service. Clients buffer out-of-order messages and deliver them in sequence order. The database stores the sequence with each message so backfill and replay preserve the same order.

**How do group chats with many members scale?**

Instead of the sender's gateway opening a socket write per member, use an internal per-group pub/sub channel or queue. Each gateway subscribes to groups where it has at least one online member and delivers locally. Recent messages are cached group-wise so offline members and new joins can backfill without hitting the database for every request.

**What is the difference between sent, delivered, and read, and how are they tracked?**

Sent means the chat service durably stored the message. Delivered means the recipient's client received it and sent an acknowledgement over the WebSocket. Read means the user opened the conversation and the client sent a read receipt with the message ID; the service updates that message's status and pushes the event back to the sender when online.

## Worked example

A strong sequence: Alice's client sends {conversation: alice-bob, clientMsgId: 723, text: "on my way"} to her gateway. The gateway forwards it to the chat service, which writes a row in the messages table with conversation_id alice-bob, sender alice, sequence 1042, content "on my way". The chat service queries the presence registry and finds bob's user ID mapped to gateway host G-7. It calls G-7 with message 1042; G-7 pushes the text over Bob's existing WebSocket. Bob's client receives it and sends ack for sequence 1042; the chat service updates the row to delivered and notifies Alice's gateway, which shows a double check. If Bob had been offline, the registry lookup would return no gateway, so the chat service would enqueue a push job; FCM sends a notification containing the message text and sequence number, and Bob's app later backfills from the database.

## Common traps

- Assuming you must shard gateways by user ID: that makes rebalancing hard after failures; use a dynamic registry that maps users to whichever gateway currently holds the socket.
- Treating push notifications as incapable of carrying text: modern APNs and FCM payloads allow up to 4 KB, enough for standard chat messages.
- Claiming a message queue gives exactly-once delivery: queues are at-least-once, so deduplicate with a client-generated message ID or store idempotency keys.
- Using a cache as the primary message store: messages must be persisted durably before delivery, or history is lost on cache eviction.

</details>

---

### 16. Horizontal scaling · Medium

*system_design · gate confidence 0.85*

<sub>to object to this card: `## sd-horizontal-scaling` then `match: A horizontally scaled web application uses a load balancer i`</sub>

**Question**

A horizontally scaled web application uses a load balancer in front of stateless application servers. The application stores session data in a shared Redis cluster. After a sudden traffic spike, users report intermittent 502 errors from the load balancer, but the application servers' CPU and memory usage remain low. What is the most likely cause?

**Options**

A. The application servers are running out of memory.
B. The Redis cluster is overloaded and rejecting session lookups.
C. The load balancer is overwhelmed or misconfigured.
D. The database connection pool is exhausted.

**Answer (the reader is graded on)**

- Correct: C. The load balancer is overwhelmed or misconfigured.

**Reference answer**

The load balancer itself is overwhelmed or misconfigured, causing it to fail to forward requests to healthy backends. Since the application servers are not resource-constrained, the bottleneck is at the load balancer, which may have hit connection limits or become a single point of failure.

**Graded on**

- 502 errors from the load balancer indicate it cannot reach a healthy backend.
- Low application server resource usage rules out backend overload.
- A single load balancer can become a bottleneck or single point of failure.

<details><summary>The lesson this came from</summary>

Horizontal scaling, or scaling out, is the practice of adding more machines or nodes to a system to handle increased load, instead of upgrading a single machine's hardware. It requires a load balancer or router to distribute work across the added nodes. This approach improves fault tolerance because a node failure does not take down the whole service, but it introduces distributed-systems complexity.

## Why interviewers ask this

Interviewers ask this to see whether you can reason about distributing a system beyond one box without glossing over shared state, load balancing, and data-layer bottlenecks. Real questions include designing a page-view counter at Booking.com and a job scheduler at Google, Amazon, Microsoft, and DoorDash, which both escalate to multi-machine consistency and cleanup.

## The core idea

Scaling out means you stop relying on one machine to do everything and instead distribute requests across many cheaper machines. The reason it works is that stateless request handling can be parallelized by a load balancer. What stays difficult is shared state: sessions, files, queues, and especially the database. So you move shared state to a separate tier that can also be partitioned or replicated. You pay for this with eventual consistency and more moving parts; you gain fault tolerance and incremental growth.

## Key points

- Horizontal scaling adds commodity machines behind a load balancer; vertical scaling adds CPU or RAM to one machine and hits a hardware ceiling.
- Application servers are typically kept stateless, with sessions in Redis, a database, or signed client tokens; sticky sessions allow local state but tie a user to an instance.
- Distribution creates coordination costs: the load balancer must be redundant, and caches or databases become the next bottleneck and may need replication, sharding, or partitioning.
- Consistent data is harder across nodes: read replicas and sharded stores often provide eventual consistency, while a single-node database provides strong consistency.
- Auto-scaling, such as Kubernetes HPA or AWS Auto Scaling, adds or removes nodes based on metrics like CPU or memory, but it is a policy layer, not inherent to horizontal scaling.

## Your 60-second answer

Horizontal scaling means adding more machines to handle more load rather than making one machine bigger. You put a load balancer in front of a pool of stateless application servers, and it distributes requests across them. The main benefit is fault tolerance and the ability to grow with commodity hardware instead of expensive specialized boxes. The trade-off is complexity: you have to externalize sessions and shared state into a store like Redis, the load balancer itself can become a single point of failure unless it is redundant, and the database or cache behind the servers becomes the next bottleneck. At the data layer you usually need read replicas, sharding, or partitioning, and you often accept eventual consistency. You scale when the bottleneck justifies it, not as premature optimization.

## If they dig deeper

**What has to change in an application to run on more than one server?**

Application servers should be stateless, or use sticky sessions or signed client tokens when they keep state locally. Any shared mutable state like sessions, uploaded files, or counters moves to a shared store such as Redis, a database, or object storage. Background jobs on a fixed schedule generally also need to become distributed or leader-elected.

**After you add web servers, what becomes the next bottleneck?**

The load balancer can become one, so production deployments use at least two with failover. More importantly, the database and cache see more concurrent connections; a single primary database can saturate. You address it with connection pooling, read replicas, caching, and eventually sharding or partitioning.

**How do you design a horizontally scalable page-view counter that only counts users active in the last five minutes?**

Keep a per-page key in a sharded Redis cluster containing a sorted set of user IDs scored by last-seen timestamp. On each view, ZADD the user ID with current time; on reload the score updates, so duplicates are naturally deduplicated. A background process removes entries older than five minutes and the count is ZCARD; if a shard fails, the count is slightly wrong, which is acceptable for this feature.

**How do you scale a job scheduler across many machines without running a job twice?**

Put jobs in a distributed queue or log such as Kafka or a cloud queue, and have worker instances consume with leases or visibility timeouts. Shard by job ID so duplicates for the same ID are handled by one consumer; use idempotency keys and a database constraint. A leader or coordination service like ZooKeeper can assign partitions, but the key is that workers claim work before executing.

**What does a control plane for a distributed database have to manage when you scale it out?**

It manages provisioning, schema changes, partition assignment, rebalancing, backups, authentication, and monitoring. Scaling out requires the control plane to coordinate shard movement without losing writes, which means using a strongly consistent metadata store like etcd or ZooKeeper and throttling rebalancing. The hardest part is avoiding split brain during partitions of the control plane itself.

## Worked example

A hotel page-view service runs 12 stateless instances behind two load balancers. When a user opens hotel 123, the instance writes to a sharded Redis cluster key `hotel:123` a sorted set member with score equal to the current epoch seconds. The same user reloading one minute later updates the same member's score, so the count does not inflate. A janitor process every 30 seconds removes members whose score is older than `now - 300`. The displayed count is `ZCARD hotel:123`, so a page can report 847 concurrent viewers. If the Redis shard holding that key is unavailable, the service returns the last cached value or a slightly stale count; because the feature tolerates approximate counts, no synchronous replication to other regions is required.

## Common traps

- Equating horizontal scaling with auto-scaling; auto-scaling is an operational policy on top, while horizontal scaling can also be done manually.
- Scaling the application tier without increasing database connection limits or adding replicas, so the primary database becomes the next bottleneck.
- Assuming every horizontal system must keep servers stateless; sticky sessions or signed client-side tokens allow some local state but create their own consistency and affinity trade-offs.
- Expecting strong consistency just because you added replicas; replication and sharding usually provide eventual consistency unless you pay for synchronous coordination.

</details>

---

## Threshold (`threshold` · pick_one)

### 17. Locking Mechanisms · Medium

*cs · gate confidence 0.9*

<sub>to object to this card: `## cs-locking-mechanisms` then `match: A transaction reads a row with version 5 and later attempts `</sub>

**Question**

A transaction reads a row with version 5 and later attempts an optimistic update with WHERE version = 5. Another transaction has already committed a change to that row, incrementing the version to 6. Under standard optimistic locking, what is the outcome of the first transaction's update?

**Options**

A. The update succeeds and overwrites the other transaction's change.
B. The update affects zero rows, indicating a conflict.
C. The update blocks until the other transaction commits.
D. The update increments the version to 7 and applies the change.

**Answer (the reader is graded on)**

- Correct: B. The update affects zero rows, indicating a conflict.

**Reference answer**

The update affects zero rows, so the transaction detects a conflict and must retry or abort. Optimistic locking validates at commit time by checking the version; since the version no longer matches, the update does not modify the row.

**Graded on**

- Optimistic locking uses a version check in the UPDATE statement.
- A mismatch means another transaction committed first.
- Zero rows affected signals a conflict.
- The transaction must re-read and retry or abort.

<details><summary>The lesson this came from</summary>

Locking mechanisms coordinate concurrent access to shared data so that only one operation that conflicts with another proceeds at a time. Pessimistic locking acquires a lock before reading or writing and holds it until commit, preventing conflicts by blocking. Optimistic locking lets transactions proceed without held locks and detects conflicts at commit time, usually by comparing a version or timestamp. Row-level locks protect individual rows, allowing other rows to be accessed concurrently, while table-level locks protect an entire table and are cheaper to manage but reduce concurrency.

## Why interviewers ask this

Interviewers use locking questions to test whether you understand concurrency control tradeoffs, not just definitions. They want to see you choose between optimistic and pessimistic strategies based on contention, and explain how lock granularity affects throughput, deadlocks, and correctness.

## The core idea

Pessimistic locking blocks early, so conflicts cannot happen, but it can cost waiting and deadlocks under contention. Optimistic locking defers conflict detection to commit, so it avoids lock overhead when conflicts are rare, but conflicting work must be rolled back and retried. Row-level locking increases concurrency because transactions touching different rows do not block each other, while table-level locking serializes entire tables, which can be acceptable for bulk operations or very low concurrency. Multi-granularity schemes use intent locks at the table level so a table-level lock request does not have to scan every row lock. Two-phase locking is a separate correctness property: acquiring all locks before releasing any guarantees conflict serializability, but does not prevent deadlocks.

## Key points

- Pessimistic locking obtains a lock before a transaction modifies data, for example using SELECT ... FOR UPDATE in SQL, and releases it at transaction end.
- Optimistic locking validates at commit time, typically by requiring UPDATE ... WHERE version = expected_version, and treats zero rows affected as a detected conflict.
- Row-level locks allow multiple transactions to modify different rows of the same table concurrently, at the cost of lock manager bookkeeping per row.
- Table-level locks are cheaper to acquire but can block operations on unrelated rows, making them more suited to bulk maintenance than fine-grained updates.
- Two-phase locking requires that no lock be acquired after any lock has been released; it ensures conflict serializability but can still deadlock.

## Your 60-second answer

Pessimistic locking assumes conflicts are likely, so the transaction acquires the lock before doing its work—for example SELECT ... FOR UPDATE—and blocks other writers until the transaction commits or rolls back. Optimistic locking assumes conflicts are rare, so transactions proceed without held locks. At commit, the update includes a version or timestamp check; if the data changed since it was read, the commit fails and the transaction retries. The main tradeoff is blocking versus wasted work: pessimistic avoids wasted work under high contention but can cause waits and deadlocks, while optimistic avoids lock overhead under low contention but repeated conflicts can force many retries. Row-level and table-level locks are a separate granularity choice. Row-level locks let transactions modify different rows concurrently at higher bookkeeping cost; table-level locks are simpler and cheaper but reduce concurrency across the whole table.

## If they dig deeper

**How do you implement optimistic locking in a relational table?**

Add a version or updated_at column. Read the version with the row, and when updating, set version = version + 1 only if version still equals the value read; check the affected row count. Zero rows means another transaction committed first, so you re-read and retry or abort.

**What is two-phase locking and why does it guarantee serializability?**

Two-phase locking splits a transaction into a growing phase where it acquires locks and a shrinking phase where it releases them, with no new lock after the first release. This prevents a cycle in the conflict graph, so the schedule is conflict-serializable. It does not prevent deadlocks; a DB must detect or use timeouts.

**How do intent locks help with mixed row and table locks?**

Before locking a row exclusively, a transaction takes an intent-exclusive lock at the table level. A later table-level lock request can check the table's intent lock rather than scanning every row lock. For example, an ALTER TABLE that needs to exclude all rows can conflict with the IX intent lock immediately.

**How does MVCC differ from pure lock-based concurrency control?**

MVCC keeps multiple versions of a row, so readers can see a consistent snapshot without acquiring shared locks. Writers still use row-level locks, but readers do not block writers and writers do not block readers under READ COMMITTED or REPEATABLE READ in PostgreSQL. Lock-based schemes traditionally require readers and writers to take conflicting locks.

**When would you choose pessimistic locking over optimistic locking despite the lock overhead?**

Choose pessimistic locking when contention is high enough that optimistic retries waste more work than blocking. It is also useful when the critical section involves external side effects or expensive computations that cannot be safely repeated. Holding locks early may be acceptable in short, high-value transactions.

## Worked example

Two transactions read an account row with id=1, balance=100, version=5. T1 executes UPDATE accounts SET balance=120, version=6 WHERE id=1 AND version=5; it affects one row and commits. T2 still holds the old snapshot version=5 and attempts UPDATE accounts SET balance=90, version=6 WHERE id=1 AND version=5; after T1's commit, this matches zero rows, so T2 knows a conflict occurred. T2 aborts its local change, re-reads the row to see balance=120 and version=6, applies any business rule against the new balance, and retries. A pessimistic approach would instead have T1 issue SELECT ... FOR UPDATE on the row when it first read, so T2 would block on that select until T1 committed and then read the current balance.

## Common traps

- Calling optimistic locking lock-free; it still takes a short write lock at commit or relies on atomic compare-and-swap, but it does not hold a lock during the read-modify-write window.
- Confusing row-level security (an access control feature that filters visible rows) with row-level locking (a concurrency control mechanism); they are unrelated despite the similar name.
- Assuming table-level locks are always a bad idea; they can be the right choice for bulk operations such as ALTER TABLE or for tables with very low concurrent access.
- Claiming two-phase locking prevents deadlocks; it guarantees conflict serializability but still allows cyclic waits that the database must detect and break by aborting a victim.

</details>

---

### 18. Database sharding · Hard

*system_design · gate confidence 0.9*

<sub>to object to this card: `## sd-database-sharding` then `match: A job scheduler stores jobs with tenant_id and due_time. You`</sub>

**Question**

A job scheduler stores jobs with tenant_id and due_time. You shard the jobs table across 4 database servers using modulo-4 hashing on tenant_id. A query asks for all jobs due before 10:00 AM. How many shards must be queried to answer this request?

**Options**

A. 1 shard
B. 2 shards
C. 3 shards
D. 4 shards

**Answer (the reader is graded on)**

- Correct: D. 4 shards

**Why (right answer, wrong reason is wrong)**

→ **A. Because due_time is not the shard key, the database cannot determine which shard contains the matching rows, so it must query every shard.**
  B. Because modulo hashing distributes rows evenly, each shard holds exactly one quarter of the jobs due before 10:00 AM.
  C. Because the query is a range scan, the database can use the shard key to route it to the shard that owns the earliest due_time.
  D. Because tenant_id is the shard key, the query can be routed to the shard that owns the tenant with the most jobs due before 10:00 AM.

**Reference answer**

All 4 shards must be queried. The shard key is tenant_id, so the due_time predicate does not determine which shard contains matching rows. The query must be sent to every shard, and the results merged.

**Graded on**

- With modulo-4 hashing on tenant_id, each shard holds a subset of tenants, not a subset of due_times.
- A query filtering on due_time cannot be routed to a single shard because due_time is not the shard key.
- The query must fan out to all 4 shards and merge the results.

<details><summary>The lesson this came from</summary>

Database sharding is horizontal partitioning: a logical table's rows are split into disjoint shards, each stored on a separate database server and holding the same schema. A shard key and routing scheme determine which shard owns a row, so a write or read can be sent directly to the right node. Sharding increases total data capacity and write throughput beyond one machine; it is distinct from replication, which copies the same rows to multiple servers. For MySQL and PostgreSQL, sharding is usually implemented in the application, via a proxy such as Vitess, or through an extension such as Citus; MongoDB has native sharded clusters.

## Why interviewers ask this

Interviewers ask this when a system design grows past a single database. They are testing whether you can choose a shard key from real access patterns, explain how a write or read gets routed, and handle the consequences: hotspots, cross-shard queries, adding capacity, and consistency. Real questions such as designing a job scheduler or a video platform reach sharding at the 'scale across machines' step.

## The core idea

Sharding is a capacity decision, not a default: you partition data only when one server plus replicas can no longer hold the working set or absorb the write load. The shard key determines which queries stay on one shard and which must fan out; choose a high-cardinality key that matches the dominant access pattern. Hash-based routing spreads writes evenly but makes range scans touch every shard; range-based routing keeps ordered scans local but risks writes stacking on one range. Moving shards is expensive, so design rebalancing before launch using consistent hashing, virtual shards, or a directory mapping. Cross-shard joins and transactions are the main recurring cost; real systems often co-locate related rows, denormalize, or aggregate in the application instead.

## Key points

- Sharding splits rows into disjoint shards on separate servers, while replication stores copies of the same rows; a sharded row's primary write goes to exactly one shard.
- A good shard key has high cardinality and aligns with the most common operations; user_id or tenant_id is usually safer than status or country because it spreads data evenly.
- Range-based sharding preserves ordered range scans but can create hotspots on monotonically increasing keys such as timestamps; hash-based sharding spreads load but forces range queries to fan out to all shards.
- Traditional sharded relational databases do not provide cross-shard ACID transactions or joins in the same way a single node does, so you must co-locate, denormalize, or use an application-level join.
- When adding a shard with simple modulo hashing, most keys move; consistent hashing or virtual shards reduce rebalancing to a fraction of keys and are common in distributed systems.

## Your 60-second answer

Sharding is horizontal partitioning: you split a table's rows across multiple database servers by a shard key, so each server holds a subset of the data and the same schema. I'd use it only after a single primary plus read replicas can't hold the data or handle write throughput. The shard key should be high cardinality and match the dominant query pattern—for a job scheduler, tenant_id keeps each tenant's operations on one shard. I'd pick range sharding when ordered scans dominate, hash sharding when I need even distribution, and a directory when I need dynamic movement. The main trade-off is that cross-shard joins and transactions become expensive, so you co-locate related data or aggregate in the application. Rebalancing is the other hard part, so I'd add consistent hashing or virtual shards early.

## If they dig deeper

**How is sharding different from replication?**

Replication keeps full copies of the same data on multiple servers and routes reads to replicas while writes go to the primary. Sharding partitions the data so each row lives on exactly one shard, and different shards handle different subsets. In production you often combine both: each shard may have its own replicas for availability.

**How do you choose a shard key?**

Pick a column that has high cardinality, distributes writes evenly, and appears in most queries. For a job scheduler, tenant_id or user_id keeps all jobs for one tenant on one shard. Avoid low-cardinality keys like status; if you need ordered scans by time but write mostly new rows, range-sharding on timestamp can create a hotspot, so hash may be better.

**What if one shard becomes a hotspot?**

Hotspots usually come from a low-cardinality key or a monotonically increasing range. You can split a hot range into smaller ranges, use a hash with a salt prefix to spread heavy keys, or add virtual shards so hot logical buckets can be moved independently. Monitor keys per shard and rebalance before a node saturates.

**How do you add a new shard without downtime?**

Use consistent hashing or a directory mapping, define the new node's token range, and migrate only the affected key ranges in the background. While migrating, dual-write to old and new shards, verify data with checksums, then atomically update the routing layer to read from the new shard and remove the old copies. Avoid simple modulo because adding a node changes almost every key's target.

**How do you handle cross-shard joins or transactions?**

In many sharded relational databases you can't run a normal SQL join across shards with full ACID, so you either denormalize and co-locate related rows on the same shard, run parallel queries and join in the application, or use a distributed SQL layer that implements cross-shard transactions with a coordinator. If strict consistency is required, look at systems designed for distributed transactions, but this adds latency.

## Worked example

Suppose a job scheduler stores jobs with tenant_id and due_time. With four shards and modulo-4 hashing on tenant_id, tenant 42 maps to shard 2 because 42 % 4 = 2, so all schedule, execute, and history queries for that tenant hit only shard 2. Tenant 43 maps to shard 3. A query for jobs due before 10:00, however, must ask all four shards because due_time is not the shard key. If instead the table is range-sharded by due_time, that query touches only the first range shard, but newly inserted jobs due at the same timestamp pile onto the current hot range. The hash design keeps per-tenant access local; the scheduler can scan each shard independently and merge due jobs.

## Common traps

- Sharding before exhausting a single server, read replicas, and caching, then paying for cross-shard complexity without needing the capacity.
- Picking a low-cardinality shard key like status or region, which creates unbalanced shards and hot nodes.
- Assuming range sharding on an auto-incrementing ID or timestamp is fine; writes concentrate on the highest range and one shard saturates.
- Adding a node by changing a modulo shard count (e.g. 4 to 5) and expecting a small migration; most rows move, requiring large data transfer.

</details>

---

## Consequence of a diff (`consequence-of-diff` · pick_one)

### 19. Deadlocks · Hard

*cs · gate confidence 0.7*

<sub>to object to this card: `## cs-deadlocks` then `match: A system currently uses deadlock prevention by imposing a gl`</sub>

**Question**

A system currently uses deadlock prevention by imposing a global lock order. The engineering team proposes switching to deadlock detection with victim rollback. Under the assumption that the workload has many short transactions that frequently contend on the same locks, what is the most likely consequence of this change?

**Options**

A. Higher concurrency but occasional transaction rollbacks.
B. Lower concurrency but no transaction rollbacks.
C. Higher concurrency and no transaction rollbacks.
D. Lower concurrency and occasional transaction rollbacks.

**Answer (the reader is graded on)**

- Correct: A. Higher concurrency but occasional transaction rollbacks.

**Why (right answer, wrong reason is wrong)**

→ **A. Detection allows transactions to acquire locks in any order, so fewer transactions are blocked waiting for locks, increasing concurrency; however, deadlocks are only resolved after they occur, so some transactions must be rolled back.**
  B. Detection requires a global lock order, which reduces the number of transactions that can run concurrently, but it eliminates deadlocks entirely, so no rollbacks are needed.
  C. Detection uses Banker's algorithm to grant locks only when safe, which increases concurrency by allowing more transactions to proceed, and because the state is always safe, no deadlocks occur.
  D. Detection periodically aborts all transactions that hold locks, which reduces concurrency because transactions are frequently restarted, and these aborts are the rollbacks observed.

**Reference answer**

The system will experience higher concurrency but occasional transaction rollbacks. Detection allows transactions to acquire locks in any order, so more can proceed simultaneously, but when a deadlock cycle forms, the detector aborts a victim, causing its work to be lost.

**Graded on**

- Prevention via lock ordering restricts concurrency because transactions must acquire locks in a fixed order, even if that means waiting for a lock they don't immediately need.
- Detection permits arbitrary lock acquisition, increasing concurrency, but deadlocks are only resolved after they occur, requiring rollback of at least one transaction.
- With many short, contending transactions, deadlocks are likely, so rollbacks will occur, but each rollback is relatively cheap because little work is lost.
- The tradeoff is between predictable, conservative execution (prevention) and higher concurrency with occasional aborts (detection).

<details><summary>The lesson this came from</summary>

A deadlock is a circular wait among processes or transactions where each holds a resource and waits for a resource held by another member of the cycle, so none can progress. It occurs only when all four Coffman conditions hold at once: mutual exclusion, hold-and-wait, no preemption, and circular wait. Systems handle deadlocks by prevention, avoidance, or detection and recovery. Prevention makes one condition impossible, avoidance grants requests only if the resulting state is safe, and detection lets cycles form then aborts victims.

## Why interviewers ask this

Interviewers ask about deadlocks to test whether you can reason about concurrent resource acquisition, not just recite definitions. They want to see you identify a circular wait in a concrete locking order and choose among prevention, avoidance, and detection based on the system's constraints. A strong answer explains the tradeoffs: prevention is predictable but conservative, detection enables more concurrency but has unpredictable rollbacks.

## The core idea

Deadlock is ultimately a cycle in the wait-for relationship: each participant holds something another waits for. You can attack it by making one of the four required conditions impossible, such as imposing a global lock order to break circular wait. Avoidance, like Banker's algorithm, allows the conditions to exist but refuses requests that could lead to an unsafe state. Detection lets cycles occur and then breaks them by terminating or rolling back at least one participant. The central tradeoff is concurrency versus predictability: prevention and avoidance reduce concurrency to avoid deadlocks, while detection preserves concurrency but accepts runtime aborts.

## Key points

- All four Coffman conditions—mutual exclusion, hold-and-wait, no preemption, and circular wait—must hold simultaneously for a deadlock; breaking any one prevents it.
- Acquiring locks in a globally consistent order is the most common way to break circular wait in practice.
- Banker's algorithm avoids deadlock by only granting a request if the resulting state remains safe, but it requires each process's maximum resource demand in advance.
- A cycle in a resource allocation graph always means deadlock only when each resource type has a single instance; with multiple instances, a cycle is necessary but not sufficient.
- Recovery selects victims by cost criteria such as priority, work done, or resources held; database transactions can roll back, while OS processes may be killed.

## Your 60-second answer

A deadlock is a circular wait where each process or transaction holds a resource another participant needs, so no one makes progress. It requires all four Coffman conditions to hold: mutual exclusion, hold-and-wait, no preemption, and circular wait. To handle it, you can prevent deadlock by making one condition impossible—usually by imposing a global lock order to break circular wait—or avoid it dynamically, as in Banker's algorithm, by granting a request only if the resulting state is safe. Alternatively, you can allow deadlocks, detect the circular wait, and recover by terminating or rolling back a victim. Prevention is simple and predictable; avoidance requires maximum resource demands; detection keeps concurrency higher but adds overhead and causes unpredictable aborts.

## If they dig deeper

**What are the four Coffman conditions required for deadlock?**

Mutual exclusion: a resource cannot be shared. Hold-and-wait: a process holds some resources while waiting for others. No preemption: a resource cannot be forcibly taken away; it is released only voluntarily. Circular wait: there is a closed chain of processes in which each waits for a resource held by the next. All four must be present at once.

**How do you prevent deadlock in code that acquires multiple locks?**

Enforce a global order on lock acquisition, such as by lock address or priority, so no two threads can hold locks in opposite order and form a cycle. If ordering is not possible, try-lock with timeouts and release all held locks on failure can break hold-and-wait. Avoiding nested locks where possible is also effective.

**Does a cycle in a resource allocation graph always indicate a deadlock?**

Only when every resource type has one instance; then each cycle is an actual permanent circular wait. With multiple instances, a cycle is necessary but not sufficient: a process in the cycle may still complete using another available instance. In that case you need a graph-reduction algorithm or Banker's-style safe-state check.

**Walk through how the Banker's algorithm decides whether a state is safe.**

Start with Work equal to Available. Repeatedly find an unfinished process whose remaining Need is less than or equal to Work, mark it finished, and add its Allocation to Work as if it released its resources. If all processes can be finished in some order, the state is safe. A request is granted only if simulating the grant leaves the system in a safe state; otherwise the requester must wait.

**Why do production databases typically use deadlock detection and rollback instead of Banker's avoidance?**

Banker's algorithm requires knowing each transaction's maximum lock demand in advance, which is impractical for ad hoc queries and dynamic workloads. Databases already track lock wait-for relationships, so they can detect a cycle and abort one transaction. For example, MySQL InnoDB detects row/table lock deadlocks and rolls back one transaction; PostgreSQL also aborts a waiting transaction on detection. This preserves more concurrency than prevention while accepting occasional rollbacks.

## Worked example

Consider a system with three resource types A, B, C and Available=(3,3,2). Five processes have allocations P0=(0,1,0), P1=(2,0,0), P2=(3,0,2), P3=(2,1,1), P4=(0,0,2) and maximum demands P0=(7,5,3), P1=(3,2,2), P2=(9,0,2), P3=(2,2,2), P4=(4,3,3). Need is max minus allocation, so P1 needs (1,2,2) and P3 needs (0,1,1). The state is safe: run P1 first, releasing (2,0,0) to make Work=(5,3,2); then P3 makes Work=(7,4,3); then P4, P0, and finally P2. Now suppose P2 requests (3,0,0). That request does not exceed its need of (6,0,0) or the available A=3, so it would be tentatively granted: available becomes (0,3,2), P2's allocation becomes (6,0,2), and P2's remaining need becomes (3,0,0). In the resulting state, only P3 can finish, after which Work=(2,4,3), but no remaining process has need ≤ Work, so the state is unsafe. Banker's algorithm therefore denies the request and leaves P2 waiting.

## Common traps

- Claiming that a cycle in a resource allocation graph always means deadlock even when resource types have multiple instances; a cycle is necessary but not sufficient in that case.
- Saying Banker's algorithm is commonly used in real operating systems, when it actually requires advance maximum resource claims and is mostly a conceptual avoidance algorithm.
- Confusing prevention with avoidance: prevention statically breaks a Coffman condition, while avoidance lets all four exist but dynamically refuses unsafe grants.
- Forgetting that breaking hold-and-wait by acquiring all resources upfront can sharply reduce concurrency and may cause starvation or indefinite waiting.

</details>

---

### 20. Lambda expressions · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-lambda-expressions` then `match: You change a lambda expression that captures a local variabl`</sub>

**Question**

You change a lambda expression that captures a local variable into an anonymous inner class that does the same thing. The local variable is effectively final. What is the most likely consequence for the captured variable?

**Options**

A. The variable can now be reassigned inside the anonymous inner class, because anonymous inner classes do not have the effectively final restriction.
B. The variable can no longer be read, because anonymous inner classes cannot capture local variables at all.
C. The variable can still be read, but `this` now refers to the anonymous inner class instance instead of the enclosing instance.
D. The variable must be declared `final` explicitly, because anonymous inner classes do not support effectively final variables.

**Answer (the reader is graded on)**

- Correct: C. The variable can still be read, but `this` now refers to the anonymous inner class instance instead of the enclosing instance.

**Reference answer**

The anonymous inner class can still read the variable, but unlike the lambda, it cannot modify it either, because anonymous inner classes also require captured local variables to be effectively final. The key difference is that the anonymous inner class has its own `this`, while the lambda's `this` refers to the enclosing instance.

**Graded on**

- Both lambdas and anonymous inner classes require captured local variables to be effectively final.
- A lambda's `this` refers to the enclosing instance, while an anonymous inner class has its own `this`.
- The change does not affect the ability to read the captured variable, only the meaning of `this`.

<details><summary>The lesson this came from</summary>

A lambda expression is a syntactic construct that creates an instance of a functional interface by supplying the body of its single abstract method inline. The arrow operator separates an optional parameter list from a body, which can be a single expression or a block. Lambda expressions were introduced in Java 8 as a concise alternative to anonymous classes that implement exactly one method.

## Why interviewers ask this

Interviewers ask about lambdas to check whether you understand Java 8's shift toward passing behavior as data and how lambdas relate to functional interfaces. They probe target typing, capture rules, and the common java.util.function interfaces because those feed directly into streams and collection pipelines.

## The core idea

In Java, a lambda expression is the body of the one abstract method in a target functional interface. The compiler uses the expected type from the assignment, cast, or method argument to infer parameter types and check return compatibility. A lambda can capture local variables only if they are effectively final—never reassigned anywhere in their scope—but it can always read and modify instance fields and static fields. At runtime, the JVM uses invokedynamic and the LambdaMetafactory to create the call site rather than generating a separate anonymous class file at compile time. A lambda body may be a single expression whose value is returned automatically, or a block with explicit returns and statements.

## Key points

- A lambda expression always implements a functional interface, which has exactly one abstract method; default and static methods do not count toward that one.
- Target typing determines the lambda's type from the surrounding context—assignment, cast, or method argument—not from the lambda's own body.
- Parameter types may be omitted, a single untyped parameter may drop parentheses, and the body can be an expression returning a value or a block with statements and explicit returns.
- Captured local variables must be effectively final, meaning they are never reassigned anywhere in their scope, while instance fields and static variables may be read and modified freely.
- Common functional interfaces include Predicate<T> with boolean test(T), Function<T,R> with R apply(T), Consumer<T> with void accept(T), and Supplier<T> with T get().

## Your 60-second answer

A lambda expression is Java's concise syntax for implementing a functional interface inline. You write the parameter list, an arrow, and a body, and the compiler treats that as providing the single abstract method of whatever functional interface is expected at that spot. For example, `Runnable r = () -> System.out.println(42);` creates a Runnable without the boilerplate of an anonymous class. Lambdas matter because they let you pass behavior as data to methods like `forEach`, `filter`, and `map`, especially with the Streams API added in Java 8. One trade-off is that they can only target interfaces with exactly one abstract method, so if you need to implement two methods you still write an anonymous class. Another trade-off is captured local variables must be effectively final, which sometimes forces a workaround like using a single-element array or a field.

## If they dig deeper

**What is a functional interface, and how does @FunctionalInterface work?**

A functional interface is an interface with exactly one abstract method. Default and static methods do not count toward that one. The @FunctionalInterface annotation is optional but when present it makes the compiler fail if the interface has zero or more than one abstract method.

**Can you assign a lambda to Object or use var with it? Why not?**

No. A lambda expression needs a target type that is a functional interface because it supplies the body of that interface's single abstract method. Object has no abstract method, so the compiler cannot infer a functional interface; you need a cast like `(Runnable) () -> ...` or an explicit functional interface target such as a variable declaration.

**What are the rules for capturing variables in a lambda expression?**

Local variables and parameters from the enclosing method can be read only if they are effectively final—never reassigned anywhere in their scope. Instance fields and static fields can always be read and modified. A lambda cannot access default methods of the functional interface it implements because there is no interface instance `this` available inside the lambda.

**How does the JVM implement lambdas differently from anonymous inner classes?**

At compile time, the compiler emits an invokedynamic call site with a method handle to a synthetic private method containing the lambda body. At runtime, the LambdaMetafactory uses that method handle to generate or return a class implementing the functional interface; no separate class file is created for each lambda, unlike anonymous inner classes which generate a distinct class at compile time.

**What are the scoping differences between a lambda and an anonymous inner class?**

A lambda is lexically scoped: `this` and `super` refer to the enclosing instance, not the lambda object, and a lambda parameter cannot shadow a local variable from the enclosing method. An anonymous inner class has its own `this`, and its parameters and locals can shadow enclosing variables because it introduces a new nested scope.

## Worked example

Take `List<String> words = Arrays.asList("apple", "pear", "kiwi");` and the call `Collections.sort(words, (a, b) -> a.length() - b.length());`. The second argument's expected type is `Comparator<String>`, whose `compare` method takes two `String` parameters and returns `int`, so the compiler infers `a` and `b` as `String` and accepts the expression body as the returned difference. If you tried to assign that same lambda to a `Function<String, Integer>`—a one-parameter interface—the parameter count mismatches and compilation fails even though an int is returned. For capturing, `int limit = 5; List<Integer> xs = Arrays.asList(1, 2, 3); xs.replaceAll(x -> x * limit);` compiles because `limit` is never reassigned; adding `limit = 6` anywhere in the method makes `limit` not effectively final and the lambda will not compile. These two examples show target typing and effective final capture.

## Common traps

- Assigning a lambda to Object or using var without a functional interface target: compilation fails because a lambda has no independent type.
- Thinking a captured local variable can be reassigned as long as the reassignment happens before the lambda: any reassignment in scope breaks effective finality, even before the lambda is created.
- Conflating lambda with anonymous inner class for `this`: inside a lambda `this` is the enclosing object, not the lambda instance.
- Using a zero-argument lambda as a Consumer: Consumer's accept method takes one argument, so `() -> list.add(x)` targets a zero-argument void interface such as Runnable, not Consumer.

</details>

---

## Missing step (`missing-step` · pick_one)

### 21. Paging and Virtual Memory · Easy

*cs · gate confidence 0.9*

<sub>to object to this card: `## cs-paging-and-virtual-memory` then `match: On x86-64 with 4-level paging and 4 KiB pages, a virtual address is split into fields. Which field is used to index the `</sub>

**Question**

On x86-64 with 4-level paging and 4 KiB pages, a virtual address is split into fields. Which field is used to index the final page table level to obtain the physical frame number?

**Options**

A. PML4 index
B. Page Directory Pointer Table index
C. Page Directory index
D. Page Table index

**Answer (the reader is graded on)**

- Correct: D. Page Table index

**Reference answer**

The Page Table (PT) index, which is the fourth 9-bit field, selects the PTE in the final level. The PTE contains the physical frame number, which is combined with the 12-bit offset to form the physical address.

**Graded on**

- The PT index is the fourth 9-bit field in a 48-bit virtual address.
- The PTE at that index provides the physical frame number.
- The offset is unchanged and appended to the frame number.

<details><summary>The lesson this came from</summary>

Virtual memory gives each process an independent virtual address space backed by physical RAM and disk. Paging splits virtual addresses into fixed-size pages and physical memory into frames of the same size; a page table maps each virtual page number to a physical frame number (PFN). The MMU performs address translation on every memory access, consulting the page table and a TLB cache of recent mappings. Demand paging loads pages from disk only when first accessed, allowing overcommit and isolation.

## Why interviewers ask this

Interviewers use this to test whether you understand the hardware-software boundary in memory management: how the MMU and OS cooperate, why TLBs are critical for performance, and what happens on a page fault. It also reveals whether you can reason about space overhead, locality, and isolation without hand-waving.

## The core idea

The key mechanism is indirection: a virtual address is split into a page number and offset; the hardware uses the page number to index a hierarchical page table, retrieves a physical frame number, and appends the unchanged offset to form the physical address. Because walking multiple levels is slow, the TLB caches recent translations, and most accesses hit. If the entry is missing or invalid, a page fault transfers control to the OS, which loads the page from disk or signals an error, then restarts the faulting instruction. This gives each process a uniform address space and lets the OS reclaim and share physical frames.

## Key points

- A page table entry stores a physical frame number (an index), not a full base address; the physical address is (PFN << page_shift) | offset.
- x86-64 4-level paging uses 48-bit virtual addresses with PML4, PDPT, PD, and PT; 5-level paging adds PML5 above PML4 for 57-bit virtual addresses.
- In Linux kernel terminology, PGD is always the top-level table: it corresponds to PML4 in 4-level mode and PML5 in 5-level mode, with P4D below PGD only in 5-level mode.
- The TLB is a small hardware cache of recent virtual-to-physical translations; on x86 the hardware walks the page table on a TLB miss, while some architectures (e.g., MIPS) use a software trap.
- Demand paging defers loading pages until first access; a page fault may also indicate a protection violation, copy-on-write, or zero-fill, not necessarily disk I/O.

## Your 60-second answer

Virtual memory gives each process its own address space, and paging maps those virtual pages to physical frames on demand. The CPU issues a virtual address; the MMU splits it into a virtual page number and an offset, looks up the page-table entry, and combines the physical frame number with the offset to form the physical address. Because page-table walks are expensive, a TLB caches recent translations so most accesses never go to memory. On a TLB miss, x86 hardware walks the multi-level table; if the entry is not present, the OS gets a page fault, loads the page from disk or swap, updates the entry, and restarts the instruction. The trade-off is translation overhead and TLB miss cost versus isolation, overcommit, and efficient use of physical memory.

## If they dig deeper

**How does the hardware split a virtual address on x86-64 with 4-level paging?**

A 48-bit virtual address is divided into five fields: four 9-bit indexes for PML4, Page Directory Pointer Table, Page Directory, and Page Table levels, plus a 12-bit offset within the 4 KiB page. Each index selects an entry in the corresponding table, and the final PTE provides the physical frame number.

**What happens on a TLB miss?**

On x86, the MMU performs a hardware page-table walk using the page-table base register and the address fields; if it finds a valid translation, it fills the TLB and retries. If any level entry is not present or has a protection violation, the hardware raises a page fault and traps to the OS.

**Why do multi-level page tables use less memory than a single flat page table for a 64-bit address space?**

A flat table for 48-bit addresses with 4 KiB pages would need 2^36 entries per process, most of which would be empty. Multi-level paging allocates only the subtrees that cover actually used virtual ranges, so sparse address spaces cost far less physical memory.

**What is the Linux kernel's naming for the levels in 5-level paging?**

Linux always calls the top-level directory PGD; in 4-level mode PGD corresponds to hardware PML4, while in 5-level mode PGD corresponds to PML5 and the level below it is P4D, which corresponds to PML4. The lower levels remain PUD, PMD, and PTE.

**How does an inverted page table differ from a normal per-process page table, and what is its main drawback?**

An inverted page table has exactly one entry per physical frame, storing the owning process ID and virtual page number, and uses hashing for lookup. It saves memory on machines with large address spaces, but makes reverse mappings and shared pages harder, and a lookup may follow a hash chain.

## Worked example

On x86-64 with 4 KiB pages and 4-level paging, a load of virtual address 0x0000_1234_5678 is split into four 9-bit table indexes and a 12-bit offset of 0x678. Assume the final PTE for the target virtual page contains a valid entry with physical frame number 0x2A. The MMU computes the physical address as (0x2A << 12) | 0x678 = 0x2A000 + 0x678 = 0x2A678, and the load proceeds. If instead that PTE has valid=0 because the page was never touched, the CPU raises a page fault; the OS allocates a free frame, reads the 4 KiB page from the executable file or swap into that frame, writes 0x2A into the PTE's PFN field with valid=1, and restarts the instruction. The same load now succeeds using the new translation.

## Common traps

- Saying the physical frame number is the full physical base address and adding it directly to the offset without shifting by the page size.
- Forgetting to invalidate the TLB on context switch or ignoring ASID tagging, which leads to stale translations from another process.
- Assuming every page fault means disk I/O; many faults are zero-fill, copy-on-write, or protection violations that need no swap.
- Proposing a single flat page table for a 64-bit address space, which would require 2^36 entries per process and be infeasible.

</details>

---

### 22. Critical Section Problem · Easy

*cs · gate confidence 0.9*

<sub>to object to this card: `## cs-critical-section-problem` then `match: Which of the following is a necessary condition for a correc`</sub>

**Question**

Which of the following is a necessary condition for a correct solution to the critical section problem?

**Options**

A. Mutual exclusion
B. No process may be starved
C. The solution must use hardware atomic instructions
D. The solution must be fair

**Answer (the reader is graded on)**

- Correct: A. Mutual exclusion

**Reference answer**

Mutual exclusion is required: at most one process may execute its critical section at a time. The other options are not necessary conditions for a correct solution.

**Graded on**

- A correct solution must guarantee mutual exclusion, progress, and bounded waiting.
- Mutual exclusion means no two processes are in their critical sections simultaneously.
- Progress and bounded waiting are also required, but they are not the only necessary conditions.

<details><summary>The lesson this came from</summary>

A critical section is a code segment in which a process accesses a shared resource, such as a variable, file, or data structure. The critical section problem is designing an entry and exit protocol so that concurrent processes execute their critical sections without corrupting shared state. A correct solution must guarantee mutual exclusion, progress, and bounded waiting.

## Why interviewers ask this

The interviewer is testing whether you understand the fundamental requirements for synchronizing concurrent access to shared data and can reason about race conditions, deadlock, and starvation. It also reveals whether you can distinguish the formal properties of a correct solution from implementation details like locks and atomic instructions.

## The core idea

The critical section problem formalizes what it means for multiple processes to safely access shared data. Mutual exclusion ensures at most one process executes its critical section at a time. The progress condition states that when no process is in the critical section and some processes want to enter, only processes not executing in their remainder sections may participate in choosing the next entrant, and that selection cannot be postponed indefinitely. Bounded waiting means that after a process requests entry, there is a finite bound on how many times other processes may enter before it does. Solutions range from software algorithms like Peterson's algorithm to hardware atomic instructions such as test-and-set and compare-and-swap, which underpin mutexes and spinlocks.

## Key points

- Mutual exclusion means no two processes may be executing inside their critical sections at the same time.
- The progress condition requires that when no process is in its critical section and some processes want to enter, only processes not executing in their remainder sections can participate in choosing the next entrant, and that choice cannot be postponed indefinitely.
- Bounded waiting means that after a process has requested entry to its critical section, there exists a finite bound on the number of times other processes may enter before it does.
- Peterson's algorithm solves the two-process case using a shared turn variable and a flag per process, but it assumes that loads and stores are atomic and not reordered.
- Hardware atomic instructions such as test-and-set or compare-and-swap are used to build spinlocks and mutexes because they make the check-and-set operation indivisible.

## Your 60-second answer

The critical section problem is coordinating access to shared data so that code that reads or modifies it runs atomically with respect to other processes. A correct solution must satisfy three conditions. Mutual exclusion: at most one process may execute its critical section at a time. Progress: if no process is in the critical section and some want to enter, only those not in their remainder sections may participate in deciding who enters next, and this decision cannot be postponed indefinitely. Bounded waiting: once a process requests entry, there is a limit on how many times other processes can enter before it does. In practice, we use mutexes, spinlocks, or atomic operations such as compare-and-swap, often supported by hardware. The main trade-off is that blocking mutexes can cause deadlock or context-switch overhead, while spinlocks waste CPU cycles on multicore systems.

## If they dig deeper

**What is the difference between deadlock and starvation in the context of critical sections?**

Deadlock occurs when processes are waiting in a cycle and none can proceed. Starvation means a process is ready but can be indefinitely bypassed by others. A solution can avoid deadlock yet still allow starvation; bounded waiting specifically rules out starvation by limiting the number of bypasses.

**Why can't disabling interrupts be used as a general user-level solution to the critical section problem?**

Disabling interrupts only stops preemption on the current core. On a multiprocessor, another core can still execute the same critical section concurrently. It is also dangerous because user code could disable interrupts for too long, and the instruction is usually privileged.

**How does Peterson's algorithm guarantee mutual exclusion for two processes?**

Each process sets its flag to indicate intent and then gives the turn to the other. Before entering, a process waits while the other's flag is set and it is the other's turn. The turn variable breaks symmetry so both cannot pass the waiting loop simultaneously, ensuring mutual exclusion.

**Why is a simple test-and-set spinlock not necessarily bounded waiting?**

A basic test-and-set lock lets a process exit and immediately re-acquire the lock before a waiting process gets scheduled, so the waiting process can be bypassed repeatedly. Bounded waiting requires a queue or another arbitration mechanism such as a ticket lock to decide the next entrant.

**Why can modern compilers or CPUs break Peterson's algorithm if memory barriers are omitted?**

They may reorder the flag write and the turn write, or reorder the flag read before the turn read, because there is no data dependence. On a weak memory model, a process may then observe the other's flag as false when it should not. Memory barriers or acquire/release semantics enforce the necessary ordering between public and private accesses.

## Worked example

Two threads share a bank balance variable initialized to 100. Each thread executes balance = balance + 1 in its critical section. Without mutual exclusion, the interleaving can be: Thread A reads 100, Thread B reads 100, Thread A writes 101, Thread B writes 101. One increment is lost; the final balance should be 102 but is 101. With a correct critical section protocol, Thread A's read-modify-write completes before Thread B starts, so B reads 101 and writes 102. This shows why the increment must be atomic with respect to other processes.

## Common traps

- Mistaking progress for simply avoiding deadlock; progress also requires that only processes not in their remainder sections participate in selecting the next entrant.
- Claiming disabling interrupts solves the problem on modern multicore systems, when it only affects the local CPU.
- Saying a standard mutex always provides bounded waiting; many implementations are not strictly FIFO and may allow a thread to be bypassed, though some provide fair locking.
- Forgetting memory ordering when explaining software mutual exclusion algorithms; compilers and CPUs can reorder independent memory operations.

</details>

---

## Next step (`next-step` · pick_one)

### 23. Deadlocks · Medium

*cs · gate confidence 0.9*

<sub>to object to this card: `## cs-deadlocks` then `match: A system uses deadlock prevention by imposing a global order`</sub>

**Question**

A system uses deadlock prevention by imposing a global order on lock acquisition. A process currently holds lock L2 and requests lock L1, where the global order is L1 < L2. According to the prevention scheme, what should the process do?

**Options**

A. Release L2, acquire L1, then reacquire L2.
B. Acquire L1 while holding L2, since the order only matters when acquiring multiple locks simultaneously.
C. Wait until L1 is available, then acquire it while still holding L2.
D. Ignore the order and acquire L1, because deadlock prevention only requires a total order, not a strict one.

**Answer (the reader is graded on)**

- Correct: A. Release L2, acquire L1, then reacquire L2.

**Reference answer**

The process must release L2, acquire L1, then reacquire L2. This maintains the global order L1 < L2, preventing circular wait. Holding L2 while waiting for L1 would violate the order and could create a deadlock cycle.

**Graded on**

- Global lock ordering requires acquiring locks in a fixed order.
- If a process holds a higher-order lock and needs a lower-order one, it must release the higher lock first.
- Releasing and reacquiring avoids holding locks in reverse order, which could lead to circular wait.

<details><summary>The lesson this came from</summary>

A deadlock is a circular wait among processes or transactions where each holds a resource and waits for a resource held by another member of the cycle, so none can progress. It occurs only when all four Coffman conditions hold at once: mutual exclusion, hold-and-wait, no preemption, and circular wait. Systems handle deadlocks by prevention, avoidance, or detection and recovery. Prevention makes one condition impossible, avoidance grants requests only if the resulting state is safe, and detection lets cycles form then aborts victims.

## Why interviewers ask this

Interviewers ask about deadlocks to test whether you can reason about concurrent resource acquisition, not just recite definitions. They want to see you identify a circular wait in a concrete locking order and choose among prevention, avoidance, and detection based on the system's constraints. A strong answer explains the tradeoffs: prevention is predictable but conservative, detection enables more concurrency but has unpredictable rollbacks.

## The core idea

Deadlock is ultimately a cycle in the wait-for relationship: each participant holds something another waits for. You can attack it by making one of the four required conditions impossible, such as imposing a global lock order to break circular wait. Avoidance, like Banker's algorithm, allows the conditions to exist but refuses requests that could lead to an unsafe state. Detection lets cycles occur and then breaks them by terminating or rolling back at least one participant. The central tradeoff is concurrency versus predictability: prevention and avoidance reduce concurrency to avoid deadlocks, while detection preserves concurrency but accepts runtime aborts.

## Key points

- All four Coffman conditions—mutual exclusion, hold-and-wait, no preemption, and circular wait—must hold simultaneously for a deadlock; breaking any one prevents it.
- Acquiring locks in a globally consistent order is the most common way to break circular wait in practice.
- Banker's algorithm avoids deadlock by only granting a request if the resulting state remains safe, but it requires each process's maximum resource demand in advance.
- A cycle in a resource allocation graph always means deadlock only when each resource type has a single instance; with multiple instances, a cycle is necessary but not sufficient.
- Recovery selects victims by cost criteria such as priority, work done, or resources held; database transactions can roll back, while OS processes may be killed.

## Your 60-second answer

A deadlock is a circular wait where each process or transaction holds a resource another participant needs, so no one makes progress. It requires all four Coffman conditions to hold: mutual exclusion, hold-and-wait, no preemption, and circular wait. To handle it, you can prevent deadlock by making one condition impossible—usually by imposing a global lock order to break circular wait—or avoid it dynamically, as in Banker's algorithm, by granting a request only if the resulting state is safe. Alternatively, you can allow deadlocks, detect the circular wait, and recover by terminating or rolling back a victim. Prevention is simple and predictable; avoidance requires maximum resource demands; detection keeps concurrency higher but adds overhead and causes unpredictable aborts.

## If they dig deeper

**What are the four Coffman conditions required for deadlock?**

Mutual exclusion: a resource cannot be shared. Hold-and-wait: a process holds some resources while waiting for others. No preemption: a resource cannot be forcibly taken away; it is released only voluntarily. Circular wait: there is a closed chain of processes in which each waits for a resource held by the next. All four must be present at once.

**How do you prevent deadlock in code that acquires multiple locks?**

Enforce a global order on lock acquisition, such as by lock address or priority, so no two threads can hold locks in opposite order and form a cycle. If ordering is not possible, try-lock with timeouts and release all held locks on failure can break hold-and-wait. Avoiding nested locks where possible is also effective.

**Does a cycle in a resource allocation graph always indicate a deadlock?**

Only when every resource type has one instance; then each cycle is an actual permanent circular wait. With multiple instances, a cycle is necessary but not sufficient: a process in the cycle may still complete using another available instance. In that case you need a graph-reduction algorithm or Banker's-style safe-state check.

**Walk through how the Banker's algorithm decides whether a state is safe.**

Start with Work equal to Available. Repeatedly find an unfinished process whose remaining Need is less than or equal to Work, mark it finished, and add its Allocation to Work as if it released its resources. If all processes can be finished in some order, the state is safe. A request is granted only if simulating the grant leaves the system in a safe state; otherwise the requester must wait.

**Why do production databases typically use deadlock detection and rollback instead of Banker's avoidance?**

Banker's algorithm requires knowing each transaction's maximum lock demand in advance, which is impractical for ad hoc queries and dynamic workloads. Databases already track lock wait-for relationships, so they can detect a cycle and abort one transaction. For example, MySQL InnoDB detects row/table lock deadlocks and rolls back one transaction; PostgreSQL also aborts a waiting transaction on detection. This preserves more concurrency than prevention while accepting occasional rollbacks.

## Worked example

Consider a system with three resource types A, B, C and Available=(3,3,2). Five processes have allocations P0=(0,1,0), P1=(2,0,0), P2=(3,0,2), P3=(2,1,1), P4=(0,0,2) and maximum demands P0=(7,5,3), P1=(3,2,2), P2=(9,0,2), P3=(2,2,2), P4=(4,3,3). Need is max minus allocation, so P1 needs (1,2,2) and P3 needs (0,1,1). The state is safe: run P1 first, releasing (2,0,0) to make Work=(5,3,2); then P3 makes Work=(7,4,3); then P4, P0, and finally P2. Now suppose P2 requests (3,0,0). That request does not exceed its need of (6,0,0) or the available A=3, so it would be tentatively granted: available becomes (0,3,2), P2's allocation becomes (6,0,2), and P2's remaining need becomes (3,0,0). In the resulting state, only P3 can finish, after which Work=(2,4,3), but no remaining process has need ≤ Work, so the state is unsafe. Banker's algorithm therefore denies the request and leaves P2 waiting.

## Common traps

- Claiming that a cycle in a resource allocation graph always means deadlock even when resource types have multiple instances; a cycle is necessary but not sufficient in that case.
- Saying Banker's algorithm is commonly used in real operating systems, when it actually requires advance maximum resource claims and is mostly a conceptual avoidance algorithm.
- Confusing prevention with avoidance: prevention statically breaks a Coffman condition, while avoidance lets all four exist but dynamically refuses unsafe grants.
- Forgetting that breaking hold-and-wait by acquiring all resources upfront can sharply reduce concurrency and may cause starvation or indefinite waiting.

</details>

---

### 24. Processes vs Threads · Medium

*cs · gate confidence 0.9*

<sub>to object to this card: `## cs-processes-vs-threads` then `match: A web server handles each request in a separate process. The`</sub>

**Question**

A web server handles each request in a separate process. The developers want to reduce memory usage and context-switching overhead while keeping the ability to run requests in parallel on multiple cores. Which change is most appropriate?

**Options**

A. Switch to a multithreaded model where each request is handled by a thread within a single process.
B. Keep the process-per-request model but use shared memory for all request data.
C. Use user-level threads within a single process to handle requests.
D. Use a single-threaded event loop to handle all requests.

**Answer (the reader is graded on)**

- Correct: A. Switch to a multithreaded model where each request is handled by a thread within a single process.

**Reference answer**

Switch to a multithreaded model where each request is handled by a thread within a single process. Threads share the process's address space, so memory overhead is lower than forking a process per request, and kernel-level threads can run in parallel on multiple cores. Context switching between threads of the same process is cheaper because the OS does not switch page tables.

**Graded on**

- Threads within a process share code, heap, and global data, reducing memory duplication.
- Kernel-level threads can be scheduled on multiple cores, enabling true parallelism.
- Thread context switches avoid page table changes, making them cheaper than process switches.

<details><summary>The lesson this came from</summary>

A process is an instance of a running program with its own virtual address space, file descriptor table, and OS resources. A thread is a schedulable execution unit inside a process; threads of the same process share the process's address space (code, heap, global data) and OS resources, but each thread has its own program counter, register set, and stack.

## Why interviewers ask this

Interviewers use this to test whether candidates understand isolation versus performance trade-offs, memory sharing, and crash semantics. Real designs such as Chrome's process-per-tab and PostgreSQL's process-per-connection rely on these trade-offs. A strong answer distinguishes communication costs, context-switching overhead, and when each concurrency model fits.

## The core idea

The fundamental difference is the memory boundary. Processes own separate address spaces, so one process cannot accidentally overwrite another's memory; this gives fault isolation but forces communication through IPC (pipes, sockets, shared memory). Threads live inside one address space and can read/write shared variables directly, which is fast but requires synchronization. Context switching between threads of the same process is cheaper because the OS does not switch page tables, only register state and stack pointers. A crash in one thread generally brings down the whole process, while a process crash is contained to that process. Choose processes for isolation and security; choose threads for shared data and low-overhead concurrency.

## Key points

- Each process has its own virtual address space, file descriptor table, and PID; threads within a process share code, heap, and open file descriptors but have private stacks, registers, and program counters.
- Context switching between two threads of the same process is cheaper than between two processes because the OS does not need to switch the address space (e.g., on x86 it does not reload CR3).
- A segmentation fault or unhandled exception in one thread typically terminates the entire process and all its threads, not just the offending thread.
- Inter-process communication requires OS mechanisms like pipes, sockets, or shared memory; threads communicate by writing to shared variables but must use synchronization (mutexes, atomics) to avoid data races.
- User-level threads are managed by a user-space library and can be scheduled quickly, but they may block the whole process on a syscall and do not give true parallelism; kernel-level threads enable parallel execution on multiple cores.

## Your 60-second answer

A process is an independent execution environment with its own virtual address space and OS resources. A thread is a schedulable unit that lives inside a process and shares its memory. Because threads share memory, they can communicate directly, but that sharing requires synchronization to avoid races. Process isolation means a crashing process doesn't affect others, but inter-process communication goes through the kernel and is slower, and process creation and context switches are more expensive. On most OSes, switching between threads of the same process avoids changing the address space, so it is cheaper. So the trade-off is isolation versus speed: use processes when you need fault containment or security boundaries, and threads when you need shared state and low overhead. That's the core of it.

## If they dig deeper

**What resources are shared between threads in the same process?**

They share the virtual address space including code, heap, and global data, as well as OS resources like the file descriptor table, signal handlers, and process ID. Each thread has its own program counter, register set, stack, and thread-local storage.

**What happens when one thread crashes compared to one process crashing?**

Most crashes, like a segmentation fault, deliver a signal to the process; by default that terminates the entire process and all threads. A separate process crash only kills that process, leaving other processes intact. This isolation is why Chrome and many web servers use process-per-tab or process-per-request.

**What is the difference between user-level and kernel-level threads?**

User-level threads are scheduled by a library in user space; the kernel sees only one process, so switching is fast but a blocking system call can stall all threads and they cannot run in parallel on multiple cores. Kernel-level threads are managed by the OS, enabling true parallelism on multiple cores and correct blocking behavior, but creation and context switching involve kernel entry, making them more expensive.

**Why can adding more threads than CPU cores sometimes reduce throughput?**

When the number of runnable threads exceeds available cores, the OS spends more time context switching and migrating threads between CPUs, which adds overhead and cache misses. Also, contention on shared locks and data structures can cause spinning or waiting, so wall-clock time may increase even though more work is attempted.

## Worked example

On Linux, fork() creates a new process with copy-on-write pages of the parent's address space. If the child modifies a global counter, the kernel copies only the affected page, so the parent's counter stays unchanged. In contrast, pthread_create() uses clone() with the CLONE_VM flag; the new thread shares the same memory pages, so a write to the global counter is immediately visible to the peer thread. For example, an in-memory session cache in a web application can be updated by any worker thread directly, but that requires a mutex to prevent two threads from corrupting the hash table. If the same server used multiple processes, each would have a private copy of the cache, and updates would require serializing the data over a pipe or shared-memory segment with synchronization. The thread approach is simpler for shared fast state but crashes together.

## Common traps

- Claiming threads share all memory including the stack; each thread actually has its own stack.
- Saying process context switch always flushes the entire TLB; modern CPUs use PCIDs or tagged TLBs, but the key difference is that thread switches avoid a page table switch.
- Assuming a crash in one thread only kills that thread; with common signals like SIGSEGV the whole process terminates.
- Ignoring that processes can share memory via shared-memory segments or mmap, so isolation is not absolute.

</details>

---

## Which invariant (`which-invariant` · pick_one)

### 25. Arrays & Hashing · Medium

*dsa · gate confidence 0.9*

<sub>to object to this card: `## arrays-hashing` then `match: You are implementing a hash table with chaining. Which invar`</sub>

**Question**

You are implementing a hash table with chaining. Which invariant must hold for the table to guarantee average O(1) lookup time?

**Options**

A. The number of buckets must be a power of two.
B. The load factor must be kept below a constant threshold, and the hash function must spread keys uniformly.
C. Every bucket must contain at most one key-value pair.
D. The hash function must be deterministic and never produce collisions.

**Answer (the reader is graded on)**

- Correct: B. The load factor must be kept below a constant threshold, and the hash function must spread keys uniformly.

**Reference answer**

The load factor must be kept below a constant threshold, and the hash function must spread keys uniformly across buckets. When the load factor stays bounded, the average chain length is O(1), so lookup is O(1) on average. If the load factor grows without bound, chains become long and lookup degrades to O(n).

**Graded on**

- Load factor = number of entries / number of buckets.
- Keeping load factor below a constant (e.g., 0.75) keeps average chain length O(1).
- A good hash function spreads keys uniformly to avoid clustering.
- Without a bounded load factor, lookup degrades to O(n) in the worst case.

<details><summary>The lesson this came from</summary>

An array is a contiguous block of same-type elements; the address of element i is base + i × element_size, so indexed read/write is O(1). A hash table uses a deterministic hash function to map a key to a bucket index, stores key-value pairs, and resolves collisions by chaining or open addressing. With good distribution and a controlled load factor, lookup, insert, and delete are O(1) on average.

## Why interviewers ask this

Interviewers at Amazon, Bloomberg, Disney, Netflix, and Apple ask array and hash problems such as Two Sum, Contains Duplicate, and Longest Consecutive Sequence to test whether you can replace an obvious O(n^2) scan with a single-pass space-for-time trade-off. They are checking fundamentals: when to use a set vs map vs array, and whether you state average vs worst-case complexity.

## The core idea

The central skill is recognizing when a nested loop can be collapsed into one pass by storing what you have already seen. If a problem asks for membership, frequency, or a complement, a hash map or set is usually the right structure. Array problems often reduce to prefix/suffix products, sorted order, or using indices to simulate multiple passes while keeping O(1) extra space. Hash table operations are average O(1), but collision handling and resizing mean worst-case O(n) unless the implementation uses balanced trees for deep buckets; say which bound you mean.

## Key points

- Array element i is addressed by base + i × element_size, giving O(1) indexed access; inserting or deleting in the middle shifts elements and is O(n).
- A hash map has average O(1) lookup, insert, and delete when the hash function spreads keys and the load factor stays low, but worst-case is O(n) if many keys collide.
- Two Sum is solved in O(n) time and O(n) space with a one-pass map from value to index, checking for target - nums[i] at each step.
- Group Anagrams can be solved in O(nk) time by encoding each string's lowercase letter counts as a key; sorting each string gives O(nk log k).
- Longest Consecutive Sequence runs in O(n) by adding all numbers to a set and only extending a streak when num - 1 is absent; each number is visited once.

## Your 60-second answer

Arrays give O(1) indexed access to contiguous elements; hash maps give average O(1) membership, insertion, and deletion by hashing a key to a bucket. The pattern is to replace a nested loop with a single pass: if I need to know whether I have seen a value or count frequencies, I store that in a hash map or set as I scan. In Two Sum, for instance, I check whether target minus the current number is already in the map, and if so return its stored index; otherwise I insert the current number with its index. That turns the obvious O(n^2) double loop into O(n) time. The cost is O(n) extra space, and the O(1) average can degrade to O(n) worst-case under many collisions.

## If they dig deeper

**What is the actual time complexity of a hash map lookup?**

Average O(1) when the hash function spreads keys and the load factor is controlled. Worst-case O(n) if many keys hash to the same bucket and the table uses chaining; Java 8+ HashMap converts buckets with more than 8 collisions into a balanced tree, giving O(log n) worst-case for that bucket.

**How do you solve Two Sum in O(n) time?**

Build a hash map from value to index in one pass. For each nums[i], if target - nums[i] is already a key, return its stored index and i; otherwise insert nums[i] -> i.

**How would you adapt Valid Anagram for Unicode characters?**

Do not use a fixed 26-element array; use a hash map from code point to count. For each character in s, increment; for each character in t, decrement; if any count is non-zero or lengths differ, they are not anagrams.

**Why is Longest Consecutive Sequence O(n) when there is a nested while loop?**

Because the while loop only runs from numbers that have no predecessor in the set, so each element is visited at most once as a streak starter and once when inside a streak; total work is O(n).

**When would you not use a hash table for membership or frequency, and what alternative would you choose?**

If you need ordered operations, range queries, or guaranteed worst-case logarithmic performance, use a balanced binary search tree or sorted array. Hash tables also have memory overhead and are not cache-friendly for iteration; a frequency array is preferable when keys are a small contiguous integer range.

## Worked example

Set answer = [1,1,1,1] for nums = [1,2,3,4]. First pass multiplies each answer[i] by the product of all elements to its left: i=0 left=1, answer[0]=1; i=1 left=1, answer[1]=1; i=2 left=2, answer[2]=2; i=3 left=6, answer[3]=6. Second pass traverses from the right, multiplying each answer[i] by the product of elements to its right: i=3 right=1, answer[3]=6; i=2 right=4, answer[2]=8; i=1 right=12, answer[1]=12; i=0 right=24, answer[0]=24. Final array [24,12,8,6] is the product of all elements except the current one.

## Common traps

- Saying hash map operations are always O(1) without mentioning worst-case O(n) collisions.
- Using a fixed 26-element count array for anagram when inputs can contain Unicode, which silently fails.
- Sorting first for Longest Consecutive Sequence gives O(n log n), violating the O(n) requirement even though it is easy.
- In Product of Array Except Self, using division and failing to handle zeros, or allocating an extra prefix array instead of using the output array for O(1) extra space.

</details>

---

### 26. Trees · Medium

*dsa · gate confidence 0.95*

<sub>to object to this card: `## trees` then `match: Which invariant must hold for a binary tree to be a valid bi`</sub>

**Question**

Which invariant must hold for a binary tree to be a valid binary search tree (BST)?

**Options**

A. Every node's left child is less than the node and its right child is greater.
B. For every node, all values in its left subtree are less than the node's value, and all values in its right subtree are greater.
C. The tree is balanced, so its height is O(log n).
D. An inorder traversal of the tree yields values in non-decreasing order.

**Answer (the reader is graded on)**

- Correct: B. For every node, all values in its left subtree are less than the node's value, and all values in its right subtree are greater.

**Reference answer**

For every node, all values in its left subtree must be less than the node's value, and all values in its right subtree must be greater. This is a global property, not just a local check between a node and its immediate children.

**Graded on**

- The BST invariant applies to entire subtrees, not just parent-child pairs.
- A node's left subtree contains only values less than the node's value.
- A node's right subtree contains only values greater than the node's value.
- Checking only immediate children can miss violations from deeper descendants.

<details><summary>The lesson this came from</summary>

In an interview context, a tree is a rooted, acyclic graph of nodes; each node stores a value and, in a binary tree, up to two child pointers labeled left and right. Many tree problems reduce to processing the root and then recursively processing the two subtrees. A binary search tree adds an ordering invariant: all values in the left subtree are less than the root and all values in the right subtree are greater. Balanced variants such as red-black trees and B-trees keep height logarithmic for systems work, but interview problems usually present plain binary trees or BSTs and ask you to reason about shape and order.

## Why interviewers ask this

Interviewers use tree problems to test whether you can decompose a recursive structure and avoid visiting nodes repeatedly, because hierarchical data appears in parsers, file systems, and database indexes. The frequency data here shows maximum path sum, BST validation, LCA, and serialization asked by companies such as DoorDash, LinkedIn, Bloomberg, Citadel, Uber, and Yahoo, so these questions also test whether you can keep per-node state and convert recursive structure to a flat format.

## The core idea

Trees are recursive by definition: the answer for a node can usually be expressed from the answers for its left and right children plus the node's own value. Pick the traversal that matches the problem; DFS is the default for recursive tree work, while BFS uses a queue when level order or breadth-related questions are asked. For a BST, inorder traversal produces sorted order, and a search can eliminate one entire subtree at every step. The biggest performance risk is shape: a tree that is unbalanced behaves like a linked list, so common tree algorithms degrade from O(log n) to O(n) in depth and sometimes O(n) stack space. Therefore, state the base case for null first, then define exactly what each recursive call returns.

## Key points

- Recursive DFS on a binary tree visits n nodes in O(n) time and uses O(h) call-stack space, where h is the tree height; for a balanced tree h is O(log n) and for a skewed tree h is O(n).
- In-order traversal of a BST yields values in strictly increasing order when duplicates are absent.
- A BST is not valid just because each immediate child is on the correct side; a node's left subtree must contain only values less than the node, which is checked by passing range bounds.
- A binary tree can be serialized with preorder traversal plus explicit null markers, and the original structure can be reconstructed in O(n) time.
- Preorder plus inorder traversal uniquely determines a binary tree when values are distinct because preorder's first element is the root and inorder splits the remaining nodes into left and right subtrees.

## Your 60-second answer

A tree is a hierarchical data structure where nodes are connected by edges, with a single root and no cycles. In coding interviews, this usually means a binary tree: each node has at most two children, and the tree is either null or a node plus two subtrees. Most problems are solved by picking a traversal, usually recursive DFS for depth-based questions or BFS with a queue for level-order questions, and then computing a result per node that gets returned up the tree. A binary search tree adds the invariant that all keys in the left subtree are less than the root and all keys in the right subtree are greater. The main trade-off is that an unbalanced tree can make DFS use O(n) stack or recursion space, while a balanced tree keeps height at O(log n) and search, insertion, and deletion in a BST become O(log n).

## If they dig deeper

**How do you compute the maximum depth of a binary tree?**

Recurse: if the node is null, return 0. Otherwise return 1 plus the maximum of the depths of the left and right children. This visits every node once, so it is O(n) time and O(h) call-stack space.

**How do you check whether a binary tree is a valid BST?**

Pass a valid range down the tree: left subtree values must be in (min, root.val) and right subtree values in (root.val, max). Comparing each node only to its direct children is not enough, because a grandchild can violate the root's bound. An inorder traversal can also work by requiring the previous value to be strictly smaller.

**How do you find the lowest common ancestor of two nodes in a BST?**

Walk from the root; if both p and q are less than the current value, move left, and if both are greater, move right. Otherwise, one value is on each side or equals the current value, so current must be the LCA. This is O(h) time and O(1) extra space.

**How do you serialize and deserialize a binary tree?**

Use preorder traversal and write a marker, often '#', for null nodes, with a delimiter between values. Deserialization consumes tokens in preorder: a marker returns null, and a value creates a node, then recursively builds left and right subtrees. That runs in O(n) time and O(n) space.

**How do you solve Binary Tree Maximum Path Sum in O(n)?**

Do a postorder traversal. At each node, clamp left and right child gains to 0 so negative single-direction paths are ignored, update the global answer with node.val + left_gain + right_gain, and return node.val + max(left_gain, right_gain) to the parent. This handles negative values correctly because an all-negative tree falls back to the largest single node.

## Worked example

Take root = [-10, 9, 20, null, null, 15, 7] from the maximum path sum problem. At leaf 15, clamped left and right gains are 0, so it returns 15; at leaf 7, it returns 7. At node 20, the left gain is 15 and the right gain is 7, so the best path that passes through 20 and splits is 15 + 20 + 7 = 42, and node 20 returns 20 + max(15, 7) = 35 to root. At root -10, the left gain from node 9 is 9 and the right gain is 35, so the best split path through root is -10 + 9 + 35 = 34. The global maximum stays 42, which is the correct answer.

## Common traps

- Checking a BST by only comparing each node with its immediate children; a value can be on the correct side of its parent and still violate an ancestor's bound.
- Using recursive DFS without acknowledging that a skewed tree of 10^4 or 10^5 nodes may exceed the call stack in some language runtimes.
- Returning the root-splitting sum from Maximum Path Sum instead of the best single-direction gain; the final path does not need to pass through the root.
- Choosing DFS where BFS is required for level-order output; DFS does not preserve sibling grouping by level.

</details>

---

## Which is not true (`which-is-not-true` · pick_one)

### 27. Deadlocks · Medium

*cs · gate confidence 0.8*

<sub>to object to this card: `## cs-deadlocks` then `match: Which of the following statements about deadlocks is NOT tru`</sub>

**Question**

Which of the following statements about deadlocks is NOT true?

**Options**

A. All four Coffman conditions must hold simultaneously for a deadlock to occur.
B. A cycle in a resource allocation graph always indicates a deadlock.
C. Banker's algorithm requires advance knowledge of each process's maximum resource demands.
D. Prevention statically breaks a Coffman condition, while avoidance dynamically refuses unsafe grants.

**Answer (the reader is graded on)**

- Correct: B. A cycle in a resource allocation graph always indicates a deadlock.

**Reference answer**

A cycle in a resource allocation graph always indicates a deadlock is not true when resource types have multiple instances; a cycle is necessary but not sufficient in that case. The other statements are correct: all four Coffman conditions must hold simultaneously, Banker's algorithm requires advance knowledge of maximum resource demands, and prevention statically breaks a Coffman condition while avoidance dynamically refuses unsafe grants.

**Graded on**

- A cycle in a resource allocation graph always means deadlock only when each resource type has a single instance.
- With multiple instances, a cycle is necessary but not sufficient for deadlock.
- Banker's algorithm requires each process's maximum resource demand in advance.
- Prevention breaks a Coffman condition statically; avoidance refuses unsafe grants dynamically.

<details><summary>The lesson this came from</summary>

A deadlock is a circular wait among processes or transactions where each holds a resource and waits for a resource held by another member of the cycle, so none can progress. It occurs only when all four Coffman conditions hold at once: mutual exclusion, hold-and-wait, no preemption, and circular wait. Systems handle deadlocks by prevention, avoidance, or detection and recovery. Prevention makes one condition impossible, avoidance grants requests only if the resulting state is safe, and detection lets cycles form then aborts victims.

## Why interviewers ask this

Interviewers ask about deadlocks to test whether you can reason about concurrent resource acquisition, not just recite definitions. They want to see you identify a circular wait in a concrete locking order and choose among prevention, avoidance, and detection based on the system's constraints. A strong answer explains the tradeoffs: prevention is predictable but conservative, detection enables more concurrency but has unpredictable rollbacks.

## The core idea

Deadlock is ultimately a cycle in the wait-for relationship: each participant holds something another waits for. You can attack it by making one of the four required conditions impossible, such as imposing a global lock order to break circular wait. Avoidance, like Banker's algorithm, allows the conditions to exist but refuses requests that could lead to an unsafe state. Detection lets cycles occur and then breaks them by terminating or rolling back at least one participant. The central tradeoff is concurrency versus predictability: prevention and avoidance reduce concurrency to avoid deadlocks, while detection preserves concurrency but accepts runtime aborts.

## Key points

- All four Coffman conditions—mutual exclusion, hold-and-wait, no preemption, and circular wait—must hold simultaneously for a deadlock; breaking any one prevents it.
- Acquiring locks in a globally consistent order is the most common way to break circular wait in practice.
- Banker's algorithm avoids deadlock by only granting a request if the resulting state remains safe, but it requires each process's maximum resource demand in advance.
- A cycle in a resource allocation graph always means deadlock only when each resource type has a single instance; with multiple instances, a cycle is necessary but not sufficient.
- Recovery selects victims by cost criteria such as priority, work done, or resources held; database transactions can roll back, while OS processes may be killed.

## Your 60-second answer

A deadlock is a circular wait where each process or transaction holds a resource another participant needs, so no one makes progress. It requires all four Coffman conditions to hold: mutual exclusion, hold-and-wait, no preemption, and circular wait. To handle it, you can prevent deadlock by making one condition impossible—usually by imposing a global lock order to break circular wait—or avoid it dynamically, as in Banker's algorithm, by granting a request only if the resulting state is safe. Alternatively, you can allow deadlocks, detect the circular wait, and recover by terminating or rolling back a victim. Prevention is simple and predictable; avoidance requires maximum resource demands; detection keeps concurrency higher but adds overhead and causes unpredictable aborts.

## If they dig deeper

**What are the four Coffman conditions required for deadlock?**

Mutual exclusion: a resource cannot be shared. Hold-and-wait: a process holds some resources while waiting for others. No preemption: a resource cannot be forcibly taken away; it is released only voluntarily. Circular wait: there is a closed chain of processes in which each waits for a resource held by the next. All four must be present at once.

**How do you prevent deadlock in code that acquires multiple locks?**

Enforce a global order on lock acquisition, such as by lock address or priority, so no two threads can hold locks in opposite order and form a cycle. If ordering is not possible, try-lock with timeouts and release all held locks on failure can break hold-and-wait. Avoiding nested locks where possible is also effective.

**Does a cycle in a resource allocation graph always indicate a deadlock?**

Only when every resource type has one instance; then each cycle is an actual permanent circular wait. With multiple instances, a cycle is necessary but not sufficient: a process in the cycle may still complete using another available instance. In that case you need a graph-reduction algorithm or Banker's-style safe-state check.

**Walk through how the Banker's algorithm decides whether a state is safe.**

Start with Work equal to Available. Repeatedly find an unfinished process whose remaining Need is less than or equal to Work, mark it finished, and add its Allocation to Work as if it released its resources. If all processes can be finished in some order, the state is safe. A request is granted only if simulating the grant leaves the system in a safe state; otherwise the requester must wait.

**Why do production databases typically use deadlock detection and rollback instead of Banker's avoidance?**

Banker's algorithm requires knowing each transaction's maximum lock demand in advance, which is impractical for ad hoc queries and dynamic workloads. Databases already track lock wait-for relationships, so they can detect a cycle and abort one transaction. For example, MySQL InnoDB detects row/table lock deadlocks and rolls back one transaction; PostgreSQL also aborts a waiting transaction on detection. This preserves more concurrency than prevention while accepting occasional rollbacks.

## Worked example

Consider a system with three resource types A, B, C and Available=(3,3,2). Five processes have allocations P0=(0,1,0), P1=(2,0,0), P2=(3,0,2), P3=(2,1,1), P4=(0,0,2) and maximum demands P0=(7,5,3), P1=(3,2,2), P2=(9,0,2), P3=(2,2,2), P4=(4,3,3). Need is max minus allocation, so P1 needs (1,2,2) and P3 needs (0,1,1). The state is safe: run P1 first, releasing (2,0,0) to make Work=(5,3,2); then P3 makes Work=(7,4,3); then P4, P0, and finally P2. Now suppose P2 requests (3,0,0). That request does not exceed its need of (6,0,0) or the available A=3, so it would be tentatively granted: available becomes (0,3,2), P2's allocation becomes (6,0,2), and P2's remaining need becomes (3,0,0). In the resulting state, only P3 can finish, after which Work=(2,4,3), but no remaining process has need ≤ Work, so the state is unsafe. Banker's algorithm therefore denies the request and leaves P2 waiting.

## Common traps

- Claiming that a cycle in a resource allocation graph always means deadlock even when resource types have multiple instances; a cycle is necessary but not sufficient in that case.
- Saying Banker's algorithm is commonly used in real operating systems, when it actually requires advance maximum resource claims and is mostly a conceptual avoidance algorithm.
- Confusing prevention with avoidance: prevention statically breaks a Coffman condition, while avoidance lets all four exist but dynamically refuses unsafe grants.
- Forgetting that breaking hold-and-wait by acquiring all resources upfront can sharply reduce concurrency and may cause starvation or indefinite waiting.

</details>

---

### 28. Collections Framework · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-collections-framework` then `match: Which of the following statements about the Java Collections Framework is NOT true?`</sub>

**Question**

Which of the following statements about the Java Collections Framework is NOT true?

**Options**

A. HashMap makes no guarantee about iteration order.
B. PriorityQueue guarantees that iterating over it yields elements in sorted order.
C. ArrayList provides O(1) get by index.
D. TreeSet stores elements in sorted order.

**Answer (the reader is graded on)**

- Correct: B. PriorityQueue guarantees that iterating over it yields elements in sorted order.

**Reference answer**

PriorityQueue does not guarantee sorted iteration order. It is a heap-based queue where only the head is guaranteed to be the least element according to natural order or a supplied comparator; iterating over the queue may yield elements in no particular order.

**Graded on**

- PriorityQueue is a heap, not a sorted structure.
- Only the head of a PriorityQueue is guaranteed to be the least element.
- Iterating a PriorityQueue does not produce sorted order.
- TreeSet or TreeMap should be used for sorted iteration.

<details><summary>The lesson this came from</summary>

The Java Collections Framework is the set of interfaces, implementations, and algorithms in java.util for representing and manipulating groups of objects as a single unit. Its core interfaces are Collection (extending Iterable) with subinterfaces List, Set, Queue, and Deque; Map is part of the framework but does not extend Collection. Concrete classes include ArrayList, LinkedList, HashSet, TreeSet, PriorityQueue, HashMap, TreeMap, and concurrent variants. The Collections utility class provides static methods such as sort, binarySearch, shuffle, and unmodifiable views.

## Why interviewers ask this

Interviewers use Collections questions to test whether you know which data structure to choose under real constraints: ordering, duplicates, null handling, thread safety, and time complexity. They also probe whether you understand the difference between interface contracts and implementation guarantees, because that is what prevents production bugs. The framework is so central to Java code that weak answers here signal weak practical Java.

## The core idea

The framework separates contracts from implementations: program to List, Set, or Map rather than to ArrayList or HashMap, so you can swap implementations. The four main data structure shapes are ordered sequences with index access (List), unique unordered or sorted elements (Set), key-value mappings (Map), and FIFO/priority task queues (Queue/Deque). Each implementation has a specific backing structure: ArrayList is a resizable array, LinkedList is a doubly-linked list, HashSet is a hash table, TreeSet is a red-black tree. Choosing a collection means matching expected operations to these underlying structures: O(1) get by index for ArrayList versus O(1) insertion at ends for LinkedList. The Collections utility class supplies polymorphic algorithms that operate on these interfaces, such as sort and binarySearch.

## Key points

- The Collection interface extends Iterable and is the root of List, Set, Queue, and Deque; Map is part of the Collections Framework but does not extend Collection.
- ArrayList is a resizable array with O(1) get/set by index and amortized O(1) add at the end, while LinkedList is a doubly-linked list with O(1) add/remove at either end.
- HashSet and HashMap provide average O(1) contains/get/put with good hash distribution but no iteration-order guarantee; LinkedHashSet and LinkedHashMap preserve insertion order.
- TreeSet and TreeMap store elements in sorted order in a red-black tree, giving O(log n) operations; a comparator or natural ordering defines the order.
- Collections is a utility class of static methods such as sort (for lists), binarySearch, shuffle, reverse, and unmodifiableList.

## Your 60-second answer

The Java Collections Framework is the set of interfaces, implementations, and algorithms in java.util for storing and manipulating groups of objects. The core interfaces are Collection, with subinterfaces List, Set, Queue, and Deque, plus Map, which is part of the framework but does not extend Collection. List gives ordered, index-based access; Set enforces uniqueness; Map stores key-value pairs; Queue handles FIFO or priority access. Choosing the right implementation depends on your operation pattern: ArrayList is a resizable array with O(1) get by index, LinkedList is a doubly-linked list with O(1) insertion at the ends, HashSet gives average O(1) contains without order, and TreeSet gives sorted order at O(log n). One trade-off is that ArrayList's fast random access costs O(n) insertion or removal in the middle, so a LinkedList may be better for frequent additions at the head or tail.

## If they dig deeper

**What is the difference between Collection and Collections?**

Collection is the root interface of most collection types, extended by List, Set, and Queue. Collections is a utility class in java.util containing static methods such as sort, binarySearch, shuffle, and unmodifiableList that operate on Collection instances. Mixing them up is a common interview slip.

**How do ArrayList and LinkedList differ in performance and when should you use each?**

ArrayList is backed by a dynamic array, so get and set by index are O(1), but inserting or removing in the middle is O(n) because elements shift. LinkedList is a doubly-linked list, so get by index is O(n), but inserting or removing at either end is O(1) and removal of a known node is O(1). Use ArrayList for random access and typical iteration, and LinkedList for frequent add/remove at the ends, like a queue or deque.

**Why is HashMap not ordered and what do LinkedHashMap and TreeMap do differently?**

HashMap spreads entries across buckets using the key's hash code, so iteration order depends on hash distribution and capacity, not insertion or sort order. LinkedHashMap maintains a doubly-linked list through entries to preserve insertion order (or access order if configured). TreeMap stores entries in a red-black tree sorted by natural key order or a comparator, giving O(log n) operations and sorted views.

**What does Collections.unmodifiableList return and can the original list still change?**

unmodifiableList returns a read-only view backed by the original list; any mutating method on the view throws UnsupportedOperationException. Changes to the underlying list are still visible through the unmodifiable view, so it is not a deep immutable copy. To prevent external mutation, do not retain a reference to the backing list.

**How is PriorityQueue different from a sorted list, and is it thread-safe?**

PriorityQueue is a heap-based queue where the head is always the least element according to natural order or a supplied comparator, but the rest of the elements are not necessarily sorted; add and poll are O(log n) and peek is O(1). Unlike a TreeSet, it allows duplicates and does not store all elements in sorted order. It is not thread-safe; use PriorityBlockingQueue for concurrent access.

## Worked example

Given an ArrayList<Integer> with five elements [10,20,30,40,50], inserting 15 at index 1 shifts elements 20 through 50 one position right, which is O(n) because all trailing elements move. A LinkedList<Integer> with the same five elements inserts at index 1 by adjusting two node references, but to reach index 1 it must traverse from the head, making add(index, element) O(n) as well. The LinkedList's O(1) insertion advantage only applies at the ends using addFirst/addLast or with an iterator at the insertion point. For a PriorityQueue<Integer> with [5,1,3], peek returns 1, the least element; after poll, the heap internally adjusts and peek returns 3.

## Common traps

- Saying Map extends Collection; Map is part of the framework but is a separate interface hierarchy, so methods like add or iterator do not apply.
- Claiming HashMap iteration order is insertion or sorted; HashMap makes no order guarantee, while LinkedHashMap preserves insertion order and TreeMap sorts keys.
- Assuming unmodifiable views are deeply immutable copies; they are backed by the original collection and reflect later changes to it.
- Using PriorityQueue for sorted iteration; it only guarantees the head is the least element, and iterating with its Iterator may yield elements in no particular order.

</details>

---

## All that apply (`all-that-apply` · claim_grid)

### 29. Service Discovery · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-service-discovery` then `match: Mark each statement as true or false.`</sub>

**Question**

Mark each statement as true or false.

**Options**

A. In client-side discovery, the client queries the registry and then calls an instance directly.
B. In server-side discovery, the client queries the registry and then calls an instance directly.
C. etcd removes a service entry when the instance's client-managed lease expires.
D. Consul cannot perform active health checks; it relies solely on client heartbeats.

**Answer (the reader is graded on)**

- In client-side discovery, the client queries the registry and then calls an instance directly. → true · In server-side discovery, the client queries the registry and then calls an instance directly. → false · etcd removes a service entry when the instance's client-managed lease expires. → true · Consul cannot perform active health checks; it relies solely on client heartbeats. → false

**Reference answer**

Statements 1 and 3 are true. Client-side discovery requires the client to query the registry and select an instance, while server-side discovery routes through a load balancer that queries the registry. etcd removes entries when a client-managed lease expires, not by actively polling HTTP health endpoints. Consul can perform active health checks, and ZooKeeper uses ephemeral znodes tied to session heartbeats.

**Graded on**

- Client-side discovery: client queries registry and calls instance directly.
- Server-side discovery: load balancer queries registry and routes.
- etcd uses leases; Consul supports active health checks.
- ZooKeeper uses ephemeral znodes tied to session heartbeats.

<details><summary>The lesson this came from</summary>

Service discovery is the component that lets a client find a live instance of a named service without hardcoded host:port pairs. Instances register with a service registry—Consul, etcd, ZooKeeper, or an orchestration API—and the registry keeps a mapping from service name to current network locations. Discovery can happen client-side, where the client queries the registry and selects an instance, or server-side, where a load balancer queries the registry and routes. Health tracking removes unreachable instances before they receive traffic.

## Why interviewers ask this

In microservices, instances scale, fail, and move; static endpoint configuration breaks under those conditions. Interviewers use service discovery to test whether you can route traffic to ephemeral instances and reason about the health and consistency paths during failure. Large system design problems often assume dynamic service locations, so a weak discovery story undermines the rest of the design.

## The core idea

Service discovery separates the identity of a service from the network location of its instances. A highly available registry stores the mapping from service name to a set of live endpoints; instances register themselves or are registered by an external controller. Health state is maintained either by leases or heartbeats from the instance, or by active checks from the registry. Clients either query the registry directly and load-balance, or delegate routing to a server-side load balancer. The hard part is consistency: a registry can only reflect change as fast as heartbeats, lease expiry, or active checks allow, so there is always a propagation delay after failure.

## Key points

- Client-side discovery has the client query the registry and then call an instance directly; server-side discovery puts a load balancer between clients and instances.
- A service registry must be highly available and up-to-date; common implementations include Consul, etcd, and ZooKeeper.
- Self-registration lets instances register and deregister themselves and send heartbeats; third-party registration uses an external controller or orchestration event to update the registry.
- etcd does not actively poll HTTP health endpoints; it deletes keys when a client-managed lease expires. Consul can perform active health checks.
- There is always a lag between an instance failing and every client stopping traffic to it, bounded by heartbeat or lease TTL plus client cache refresh.

## Your 60-second answer

Service discovery is how a service finds the current network location of another service instance without hardcoded addresses. Each instance registers in a service registry—Consul, etcd, or ZooKeeper—which stores the mapping from service name to live host:port endpoints, and removes entries when instances fail health checks or miss heartbeats. In client-side discovery, the caller queries the registry and selects an instance; in server-side discovery, a load balancer queries the registry and routes the request. Registration can be self-registration by the instance or third-party registration by an orchestrator. The main trade-off is freshness versus availability: a registry can only reflect failure as fast as its TTL or check interval, so clients may briefly call an instance that is already down unless they retry or fall back.

## If they dig deeper

**What is the difference between client-side and server-side discovery?**

In client-side discovery, the client queries the registry, obtains the list of instances, and performs load balancing itself before calling the instance directly. In server-side discovery, the client sends the request to a load balancer or router, which queries the registry and forwards traffic to a chosen instance. Client-side discovery gives clients more control and removes a network hop, but requires a discovery client and load-balancing logic in every service.

**How do instances register themselves, and what are the alternatives?**

Self-registration means the instance calls the registry on startup, deregisters on shutdown, and may send heartbeats. Third-party registration uses an external controller or orchestration platform, such as Kubernetes, to detect containers and update the registry. Self-registration couples the service to the registry; third-party registration centralizes lifecycle awareness but can miss an unhealthy process if the container still exists.

**How does the registry know if an instance is still healthy?**

It depends on the registry. Consul can run active health checks, such as HTTP probes, and mark instances unhealthy after repeated failures. etcd uses client-managed leases: the instance must refresh its lease with keep-alives before TTL expiry, otherwise the key is deleted. ZooKeeper uses ephemeral znodes tied to a session heartbeat. Active checks can test external dependencies; lease expiration only proves the client process can still reach the registry.

**What happens if the service registry itself goes down?**

A strong answer distinguishes the control plane from the data plane. Existing clients may keep using cached endpoints, and server-side load balancers may keep routing from their last known table, so traffic can continue temporarily. New instances cannot register and old ones cannot deregister until the registry recovers, so changes are frozen and failures may not be removed. For this reason the registry is typically run as a small replicated highly available cluster and treated as critical infrastructure.

**How do you avoid a thundering herd of clients querying the registry on every request?**

Clients cache the endpoint list and subscribe to updates or refresh lazily with a bounded TTL or jitter. In server-side discovery, only the load balancer queries the registry, so client fan-out is much smaller. Service meshes push endpoint updates to sidecar proxies through the control plane, avoiding repeated polling. The tradeoff is cache staleness: after a failure, some requests may still target the dead instance until refresh.

## Worked example

Consider a payments service with three instances, each registered under the same service name and sending keep-alives every 3 seconds. The registry lease has a TTL of 10 seconds. A client caches the endpoint list for 30 seconds and load-balances across the instances. If instance B crashes at t=0 and its last keep-alive was at t=0, the registry deletes it when the lease expires at about t=10; before that, the registry still lists B. If the client last refreshed at t=-5, it will keep a cached list containing B until t=25, so it can still call the dead instance. That window is why client-side discovery needs retries or a fallback path, while server-side load balancers can perform active health checks and remove B sooner.

## Common traps

- Assuming every registry actively health-checks instances: etcd uses leases, while Consul supports active HTTP and TCP checks.
- Hardcoding service endpoints in configuration and calling that service discovery: it breaks when instances scale or move.
- Confusing the registry with the load balancer: in client-side discovery, clients query the registry but still call instances directly.
- Forgetting cache staleness: a client with cached endpoints can keep sending traffic to a dead instance after the registry removes it.

</details>

---

### 30. HashMap internals · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-hashmap-internals` then `match: Which of the following statements about Java HashMap interna`</sub>

**Question**

Which of the following statements about Java HashMap internals are true? Mark each statement as true or false.

**Options**

A. A bucket is converted to a red-black tree only when it already has 8 linked nodes before insertion and the bucket array has at least 64 slots.
B. A bucket with 8 linked nodes is always converted to a red-black tree, regardless of the bucket array size.
C. When the table is resized, each old bucket's entries split into either the original index or original index + old capacity.
D. During a resize, a tree portion with 8 or fewer nodes is converted back to a linked list.

**Answer (the reader is graded on)**

- A bucket is converted to a red-black tree only when it already has 8 linked nodes before insertion and the bucket array has at least 64 slots. → true · A bucket with 8 linked nodes is always converted to a red-black tree, regardless of the bucket array size. → false · When the table is resized, each old bucket's entries split into either the original index or original index + old capacity. → true · During a resize, a tree portion with 8 or fewer nodes is converted back to a linked list. → false

**Reference answer**

Statements 1 and 3 are true. A bucket is treeified only when it already has 8 linked nodes before insertion and the table has at least 64 slots. During resize, each old bucket splits into two buckets using the old-capacity bit of the hash. Statement 2 is false because treeification requires both conditions, not just bucket depth. Statement 4 is false because a tree bin is untreeified during resize if a split portion has 6 or fewer nodes, not 8.

**Graded on**

- Treeification requires bucket depth ≥ 8 and table size ≥ 64.
- Resize splits each bucket into original index or original index + old capacity.
- During resize, a tree portion with ≤ 6 nodes becomes a linked list.

<details><summary>The lesson this came from</summary>

Java's HashMap is a hash table backed by an array of buckets. For a key, it computes a spread hash from key.hashCode() and chooses a bucket with (capacity - 1) & hash. Each bucket holds a linked list of Node entries; in Java 8+, a bucket that already has 8 nodes before another insertion is converted to a red-black tree only when the bucket array has at least 64 slots. Lookup walks the bucket using equals(). Resize doubles the array when size exceeds capacity * loadFactor (default 0.75), redistributing entries. Before Java 8, buckets were linked lists only, so worst-case lookup was O(n).

## Why interviewers ask this

The interviewer is checking whether the candidate understands why HashMap is average O(1), what can degrade it, and how equals/hashCode interact. They also want to see awareness that Java 8 changed collision behavior from pure linked lists to tree bins, which changes worst-case lookup from O(n) to O(log n).

## The core idea

HashMap is an array of buckets; the key's hash chooses the bucket and equals() picks the exact entry. Java's implementation mixes high bits of the hash into the low bits before masking with capacity-1, so small tables still distribute well. Each bucket begins as a linked list; Java 8 promotes a bucket to a red-black tree only when it already has 8 nodes and the table is at least 64 slots, which changes worst-case lookup from O(n) to O(log n). Resizing doubles the table, and each bucket splits into two buckets using the old-capacity bit of the hash, without rehashing. Tree bins split carefully: split portions with 6 or fewer nodes become linked lists, while removal untreeifies when root or immediate structural children are null.

## Key points

- In Java 8+, a HashMap bucket is a linked list that is converted into a red-black tree only when the bucket already has 8 linked nodes before inserting the next one, and the bucket array length is at least 64.
- Bucket index is (n - 1) & (key.hashCode() ^ (key.hashCode() >>> 16)), so high bits of the hash influence the index even when n is small.
- When resize doubles the table, each old bucket's entries split into either the original index or original index + old capacity, depending on one extra hash bit.
- During a resize split, a tree portion with 6 or fewer nodes is converted back to a linked list; in a non-resize removal, a tree bin is untreeified if the root is null, root.right is null, root.left is null, or root.left.left is null.
- Retrieval requires both hashCode to locate the bucket and equals to identify the key, so keys should be immutable and have consistent hashCode/equals.

## Your 60-second answer

A HashMap is an array of buckets. On put, Java hashes the key, spreads the hash, and uses the low bits to pick a bucket. Inside the bucket, entries are stored as linked nodes; in Java 8 a bucket that already has 8 nodes and sits in a table with at least 64 slots becomes a red-black tree, changing worst-case lookup from O(n) to O(log n). Get recomputes the bucket and then uses equals to find the exact key, so hashCode and equals must be consistent. When the map crosses its load factor, the array doubles, and each old bucket splits into its original index or that index plus the old capacity. That keeps the table sparse enough for average O(1) behavior. The main tradeoff is memory: tree nodes are larger than plain list nodes, so the threshold avoids wasting memory when keys are well distributed.

## If they dig deeper

**What is the role of hashCode and equals when you use a key in HashMap?**

hashCode locates the bucket; equals distinguishes keys within that bucket. Equal keys must have equal hash codes, but unequal keys may still collide. If equals is overridden without hashCode, equal keys can land in different buckets and be lost.

**Why does HashMap keep bucket array size a power of two?**

A power-of-two capacity lets the map compute bucket index with (capacity - 1) & hash instead of a modulo, which is faster and avoids negative hash handling. It also makes resize split each old bucket into two using just the old-capacity bit, so entries move to the original index or original index + old capacity without recomputing hashes.

**What exactly triggers treeification in Java 8, and why is the table size condition there?**

When a bucket already has 8 linked nodes and a new insertion arrives, if the bucket array length is at least 64, the list becomes a red-black tree; if the table is smaller, resize is preferred because expanding the whole table may reduce collisions more cheaply. Tree nodes are about twice the size of list nodes, so treeification is only worthwhile for large bins.

**When does a tree bin turn back into a linked list?**

During resize, a TreeNode split checks the size of each portion: a portion with 6 or fewer nodes is untreeified. During remove, untreeification is not directly a countdown to 6; it checks structural conditions: if the root, root.right, root.left, or root.left.left is null, the tree is too small or degenerate and is replaced by a linked list.

**How would you implement a custom key class correctly, and what happens if you mutate an already-inserted key?**

You must override equals and hashCode consistently and make the key immutable or prevent mutation of fields used in hashCode. If you mutate a key after insertion, its hash changes, so the entry remains in the old bucket; get may compute a different bucket and return null, causing the entry to be leaked until a resize or manual removal.

## Worked example

Suppose a HashMap has capacity 16. Put key K1 with hashCode 1 and key K2 with hashCode 17. The spread step leaves these as 1 and 17; bucket index for both is (16 - 1) & hash: 15 & 1 = 1 and 15 & 17 = 1, so they collide in bucket 1. The map stores K1's Node, then during put of K2, it traverses the linked list in bucket 1; since K1.equals(K2) is false, it appends K2. A get for K2 computes index 1, walks the chain comparing equals, and returns K2's value. Later, if the table resizes to 32, the old bucket 1 splits: entries whose hash has bit 16 set (like 17) move to index 1 + 16 = 17; hash 1 stays at index 1. Because capacity-1 changes from 15 to 31, index becomes hash & 31.

## Common traps

- Claiming HashMap lookup is always O(1); a bad hashCode or large collisions can degrade to O(n) in Java 7 or O(log n) in Java 8 tree bins.
- Forgetting that treeification requires both bucket depth and minimum table size (64); many candidates say any 8-element list becomes a tree immediately.
- Using a mutable key after insertion; the key's new hash changes bucket, so the entry becomes unreachable by get and leaks.
- Saying HashMap allows multiple null keys; it permits exactly one null key and multiple null values.

</details>

---

## Which invariants hold (`which-invariants-hold` · claim_grid)

### 31. String · Medium

*dsa · gate confidence 0.8*

<sub>to object to this card: `## string` then `match: Which of the following statements about strings are true? Ma`</sub>

**Question**

Which of the following statements about strings are true? Mark each statement as true or false.

**Options**

A. In Java and Python, strings are immutable, so repeated concatenation with `+` inside a loop is O(n^2).
B. KMP substring search runs in O(n+m) worst-case time.
C. In C++, `std::string` is mutable and supports in-place modification.
D. In Java, `==` compares string content, so two distinct `new String("abc")` objects are equal.

**Answer (the reader is graded on)**

- In Java and Python, strings are immutable, so repeated concatenation with `+` inside a loop is O(n^2). → true · KMP substring search runs in O(n+m) worst-case time. → true · In C++, `std::string` is mutable and supports in-place modification. → true · In Java, `==` compares string content, so two distinct `new String("abc")` objects are equal. → false

**Reference answer**

The true statements are: (1) In Java and Python, strings are immutable, so repeated concatenation with `+` inside a loop is O(n^2). (2) KMP substring search runs in O(n+m) worst-case time. (3) In C++, `std::string` is mutable and supports in-place modification. The false statement is: (4) In Java, `==` compares string content, so two distinct `new String("abc")` objects are equal.

**Graded on**

- Java and Python strings are immutable; `+` in a loop creates a new string each iteration, leading to O(n^2) time.
- KMP preprocesses the pattern and scans the text in O(n+m) worst-case time.
- C++ `std::string` is mutable, allowing in-place operations like reversing words with O(1) extra space.
- In Java, `==` compares references, not content; use `.equals()` for content comparison.

<details><summary>The lesson this came from</summary>

A string is a sequence of characters, generally stored as an array of code units. In most interview languages, strings are immutable objects (Java, Python) or mutable sequences (C++ std::string). Because they are arrays of characters, array techniques—two pointers, sliding windows, recursion—apply, but parsing and substring search have string-specific edge cases.

## Why interviewers ask this

Interviewers use string problems to test careful edge-case handling (atoi, valid number), modular string construction (integer to words, count and say), and substring algorithms (KMP, Rabin-Karp, sliding window). Companies like Meta, Netflix, Apple, and Bloomberg ask these because strings appear in parsing, logs, and text processing.

## The core idea

Treat a string as an immutable array; know how immutability changes complexity. Building a string by repeated concatenation in a loop is O(n^2) in Java and Python; use StringBuilder or list/join. Parsing problems are deterministic state machines: skip whitespace, sign, digits, then handle overflow before the value can wrap. For substring constraints, sliding windows with hashmaps solve many linear-time problems; for exact pattern matching, KMP gives guaranteed O(n+m) while Rabin-Karp uses hashing with expected O(n+m).

## Key points

- In Java and Python, strings are immutable; using `+` to build a string inside a loop typically creates a new object each iteration, making the operation O(n^2) rather than O(n).
- In C++, `std::string` is mutable and supports in-place modification, so solutions like reversing words can use O(1) extra space by reversing and then trimming.
- Parsing a numeric string must handle overflow before multiplying by 10; checking `current > (INT_MAX - digit) / 10` prevents wrapping.
- For substring search, KMP preprocesses the pattern into a prefix table and scans text in O(n+m) worst case, while Rabin-Karp uses a rolling hash in O(n+m) expected time but can degrade on collisions.
- In Java, comparing string content requires `.equals()`; `==` compares object references and often fails for distinct `new String` objects.

## Your 60-second answer

Strings are sequences of characters, so I treat them like arrays, but with immutability in Java and Python. That means building a string with plus inside a loop is quadratic, so I use StringBuilder or join a list instead. For parsing problems like atoi, I follow a small state machine: skip leading whitespace, read an optional sign, accumulate digits while checking overflow before each multiplication, then clamp to the 32-bit range. For substring problems, a sliding window with hash maps handles many constraints in linear time, and for exact pattern matching KMP gives guaranteed O(n+m) while Rabin-Karp is often simpler with a rolling hash. The main trade-off is that mutability differs by language, so I check whether in-place operations are allowed.

## If they dig deeper

**Why do you recommend StringBuilder over string concatenation in a loop?**

In Java, String is immutable, so each `+` creates a new String and copies all previous characters. A loop of n concatenations therefore runs in O(n^2). StringBuilder is mutable and appends in amortized O(1), making the whole loop O(n).

**How would you solve Reverse Words in a String in-place if the string is mutable?**

Reverse the entire character array, then scan to reverse each word individually. Finally remove or compact extra spaces by shifting characters left. This runs in O(n) time and O(1) extra space.

**What is the difference between KMP and Rabin-Karp for substring search?**

KMP preprocesses the pattern into a prefix function and scans the text in O(n+m) worst-case time, with no false positives. Rabin-Karp hashes substrings with a rolling hash, giving O(n+m) expected time and O(1) extra space, but hash collisions can cause worst-case O(nm).

**For the at-least-K repeating characters problem, why does the sliding window over unique character counts give O(n) time?**

Since the alphabet is lowercase English, there are at most 26 unique characters. We run the sliding window once for each allowed number of unique characters, from 1 to 26. Each pass is O(n), so total is O(26n) = O(n), with O(1) extra space besides a fixed-size count array.

**How does an immutable string affect solutions that appear to modify the string in place?**

In Java and Python, there is no in-place mutation; you must allocate a new string or use a mutable builder. An algorithm described as in-place for C++ must be adapted to copy-on-write semantics, often using a char array or list, and the resulting complexity may include O(n) extra space for the converted structure.

## Worked example

For `myAtoi` with input `"   -0042abc"`, the algorithm first skips three spaces, reads the sign `-`, then processes digits: 0, 0, 4, 2. The accumulated value starts at 0 and updates as `0*10+0=0`, `0*10+0=0`, `0*10+4=4`, `4*10+2=42`. It stops at `a` because a non-digit ends the digit sequence. Applying the sign gives `-42`. Before each update, it checks `value > (INT_MAX - digit) / 10`; for input `"2147483648"` this check triggers before appending the final digit and returns `INT_MAX` instead of wrapping to a negative number. The entire scan is O(n) time and O(1) space.

## Common traps

- Using `==` to compare Java Strings; it checks reference equality, so two distinct `new String("abc")` objects are not equal even though content matches.
- Building strings with `+` in loops in Java or Python, causing O(n^2) time because each concatenation allocates a new immutable string.
- Forgetting the overflow check before `num = num * 10 + digit` in atoi; the intermediate multiplication can overflow a 32-bit or even 64-bit accumulator.
- Assuming that `s.length` counts user-perceived characters in Java/Python; for emoji or other supplementary Unicode, it counts UTF-16 code units or code points, not grapheme clusters.

</details>

---

### 32. Deadlocks · Hard

*cs · gate confidence 0.8*

<sub>to object to this card: `## cs-deadlocks` then `match: Consider a system with multiple resource types, some with mu`</sub>

**Question**

Consider a system with multiple resource types, some with multiple instances. For each statement, mark whether it is true or false.

**Options**

A. A cycle in a resource allocation graph always indicates a deadlock, regardless of the number of instances of each resource type.
B. Banker's algorithm requires each process to declare its maximum resource needs in advance.
C. Deadlock prevention and avoidance are the same: both dynamically refuse resource requests that could lead to an unsafe state.
D. Imposing a global order on lock acquisition breaks the circular wait condition.

**Answer (the reader is graded on)**

- A cycle in a resource allocation graph always indicates a deadlock, regardless of the number of instances of each resource type. → false · Banker's algorithm requires each process to declare its maximum resource needs in advance. → true · Deadlock prevention and avoidance are the same: both dynamically refuse resource requests that could lead to an unsafe state. → false · Imposing a global order on lock acquisition breaks the circular wait condition. → true

**Why (right answer, wrong reason is wrong)**

→ **A. A cycle in a resource allocation graph is sufficient for deadlock only when each resource type has a single instance; with multiple instances, a process in the cycle may complete using another available instance.**
  B. A cycle in a resource allocation graph is sufficient for deadlock regardless of the number of instances because the cycle itself prevents any process from releasing resources.
  C. A cycle in a resource allocation graph is sufficient for deadlock only when each resource type has a single instance; with multiple instances, a cycle is impossible.
  D. A cycle in a resource allocation graph is sufficient for deadlock regardless of the number of instances because all processes in the cycle are permanently blocked.

**Reference answer**

Statement 1 is false: a cycle in a resource allocation graph is necessary but not sufficient for deadlock when resource types have multiple instances. Statement 2 is true: Banker's algorithm requires each process to declare its maximum resource needs in advance. Statement 3 is false: prevention breaks one of the Coffman conditions statically, while avoidance dynamically refuses unsafe grants. Statement 4 is true: a global lock order breaks circular wait, one of the four Coffman conditions.

**Graded on**

- A cycle in a resource allocation graph is necessary but not sufficient for deadlock when resource types have multiple instances.
- Banker's algorithm requires advance knowledge of each process's maximum resource demand.
- Prevention statically breaks a Coffman condition; avoidance dynamically refuses unsafe grants.
- A global lock order breaks circular wait, one of the four Coffman conditions.

<details><summary>The lesson this came from</summary>

A deadlock is a circular wait among processes or transactions where each holds a resource and waits for a resource held by another member of the cycle, so none can progress. It occurs only when all four Coffman conditions hold at once: mutual exclusion, hold-and-wait, no preemption, and circular wait. Systems handle deadlocks by prevention, avoidance, or detection and recovery. Prevention makes one condition impossible, avoidance grants requests only if the resulting state is safe, and detection lets cycles form then aborts victims.

## Why interviewers ask this

Interviewers ask about deadlocks to test whether you can reason about concurrent resource acquisition, not just recite definitions. They want to see you identify a circular wait in a concrete locking order and choose among prevention, avoidance, and detection based on the system's constraints. A strong answer explains the tradeoffs: prevention is predictable but conservative, detection enables more concurrency but has unpredictable rollbacks.

## The core idea

Deadlock is ultimately a cycle in the wait-for relationship: each participant holds something another waits for. You can attack it by making one of the four required conditions impossible, such as imposing a global lock order to break circular wait. Avoidance, like Banker's algorithm, allows the conditions to exist but refuses requests that could lead to an unsafe state. Detection lets cycles occur and then breaks them by terminating or rolling back at least one participant. The central tradeoff is concurrency versus predictability: prevention and avoidance reduce concurrency to avoid deadlocks, while detection preserves concurrency but accepts runtime aborts.

## Key points

- All four Coffman conditions—mutual exclusion, hold-and-wait, no preemption, and circular wait—must hold simultaneously for a deadlock; breaking any one prevents it.
- Acquiring locks in a globally consistent order is the most common way to break circular wait in practice.
- Banker's algorithm avoids deadlock by only granting a request if the resulting state remains safe, but it requires each process's maximum resource demand in advance.
- A cycle in a resource allocation graph always means deadlock only when each resource type has a single instance; with multiple instances, a cycle is necessary but not sufficient.
- Recovery selects victims by cost criteria such as priority, work done, or resources held; database transactions can roll back, while OS processes may be killed.

## Your 60-second answer

A deadlock is a circular wait where each process or transaction holds a resource another participant needs, so no one makes progress. It requires all four Coffman conditions to hold: mutual exclusion, hold-and-wait, no preemption, and circular wait. To handle it, you can prevent deadlock by making one condition impossible—usually by imposing a global lock order to break circular wait—or avoid it dynamically, as in Banker's algorithm, by granting a request only if the resulting state is safe. Alternatively, you can allow deadlocks, detect the circular wait, and recover by terminating or rolling back a victim. Prevention is simple and predictable; avoidance requires maximum resource demands; detection keeps concurrency higher but adds overhead and causes unpredictable aborts.

## If they dig deeper

**What are the four Coffman conditions required for deadlock?**

Mutual exclusion: a resource cannot be shared. Hold-and-wait: a process holds some resources while waiting for others. No preemption: a resource cannot be forcibly taken away; it is released only voluntarily. Circular wait: there is a closed chain of processes in which each waits for a resource held by the next. All four must be present at once.

**How do you prevent deadlock in code that acquires multiple locks?**

Enforce a global order on lock acquisition, such as by lock address or priority, so no two threads can hold locks in opposite order and form a cycle. If ordering is not possible, try-lock with timeouts and release all held locks on failure can break hold-and-wait. Avoiding nested locks where possible is also effective.

**Does a cycle in a resource allocation graph always indicate a deadlock?**

Only when every resource type has one instance; then each cycle is an actual permanent circular wait. With multiple instances, a cycle is necessary but not sufficient: a process in the cycle may still complete using another available instance. In that case you need a graph-reduction algorithm or Banker's-style safe-state check.

**Walk through how the Banker's algorithm decides whether a state is safe.**

Start with Work equal to Available. Repeatedly find an unfinished process whose remaining Need is less than or equal to Work, mark it finished, and add its Allocation to Work as if it released its resources. If all processes can be finished in some order, the state is safe. A request is granted only if simulating the grant leaves the system in a safe state; otherwise the requester must wait.

**Why do production databases typically use deadlock detection and rollback instead of Banker's avoidance?**

Banker's algorithm requires knowing each transaction's maximum lock demand in advance, which is impractical for ad hoc queries and dynamic workloads. Databases already track lock wait-for relationships, so they can detect a cycle and abort one transaction. For example, MySQL InnoDB detects row/table lock deadlocks and rolls back one transaction; PostgreSQL also aborts a waiting transaction on detection. This preserves more concurrency than prevention while accepting occasional rollbacks.

## Worked example

Consider a system with three resource types A, B, C and Available=(3,3,2). Five processes have allocations P0=(0,1,0), P1=(2,0,0), P2=(3,0,2), P3=(2,1,1), P4=(0,0,2) and maximum demands P0=(7,5,3), P1=(3,2,2), P2=(9,0,2), P3=(2,2,2), P4=(4,3,3). Need is max minus allocation, so P1 needs (1,2,2) and P3 needs (0,1,1). The state is safe: run P1 first, releasing (2,0,0) to make Work=(5,3,2); then P3 makes Work=(7,4,3); then P4, P0, and finally P2. Now suppose P2 requests (3,0,0). That request does not exceed its need of (6,0,0) or the available A=3, so it would be tentatively granted: available becomes (0,3,2), P2's allocation becomes (6,0,2), and P2's remaining need becomes (3,0,0). In the resulting state, only P3 can finish, after which Work=(2,4,3), but no remaining process has need ≤ Work, so the state is unsafe. Banker's algorithm therefore denies the request and leaves P2 waiting.

## Common traps

- Claiming that a cycle in a resource allocation graph always means deadlock even when resource types have multiple instances; a cycle is necessary but not sufficient in that case.
- Saying Banker's algorithm is commonly used in real operating systems, when it actually requires advance maximum resource claims and is mostly a conceptual avoidance algorithm.
- Confusing prevention with avoidance: prevention statically breaks a Coffman condition, while avoidance lets all four exist but dynamically refuses unsafe grants.
- Forgetting that breaking hold-and-wait by acquiring all resources upfront can sharply reduce concurrency and may cause starvation or indefinite waiting.

</details>

---

## Sequence (`sequence` · order)

### 33. Correlated vs nested subqueries · Medium

*sql · gate confidence 0.8*

<sub>to object to this card: `## sql-correlated-vs-nested-subqueries` then `match: Arrange the following steps in the order they occur when a database executes a correlated `</sub>

**Question**

Arrange the following steps in the order they occur when a database executes a correlated subquery, assuming the optimizer does not decorrelate it. Start with the first step.

**Options**

A. The inner query's result is used to evaluate the outer row's predicate.
B. The outer query produces a row from its driving table.
C. The inner query is evaluated using those values.
D. The current row's column values are passed into the inner query.

**Answer (the reader is graded on)**

- before: The outer query produces a row from its driving table. → The current row's column values are passed into the inner query. · The current row's column values are passed into the inner query. → The inner query is evaluated using those values. · The inner query is evaluated using those values. → The inner query's result is used to evaluate the outer row's predicate.

**Reference answer**

The correct order is: (1) The outer query produces a row from its driving table. (2) The current row's column values are passed into the inner query. (3) The inner query is evaluated using those values. (4) The inner query's result is used to evaluate the outer row's predicate. This repeats for each outer row.

**Graded on**

- A correlated subquery is logically evaluated once per outer row.
- The inner query cannot run standalone because it references outer columns.
- The outer row's values are passed into the inner query for each evaluation.
- The inner result determines whether the outer row is included or affected.

<details><summary>The lesson this came from</summary>

A nested (non-correlated) subquery is a SELECT placed inside another statement; it contains no reference to outer-query columns, so it can execute once and return a scalar value or a set of rows for the outer query. A correlated subquery has a predicate that references at least one column from an outer query, which makes it logically evaluated once for each row of the outer SELECT, UPDATE, or DELETE. Correlation is determined by column references, not by how deeply the query is nested. A correlated subquery cannot be executed in isolation.

## Why interviewers ask this

The interviewer is checking whether you can read a query and identify which subquery is correlated by spotting outer-column references. They also expect you to explain the execution model: an independent inner query runs once, while a correlated inner query is repeated per outer row. This usually leads into performance trade-offs and whether you know how to rewrite with JOIN, GROUP BY, or window functions.

## The core idea

A subquery is correlated exactly when its inner query references a column from an outer query block. That dependency means the inner query cannot be prepared as a standalone result; the DBMS conceptually executes it once per outer row, passing the current row's values each time. A non-correlated nested subquery has no such dependency, so it is evaluated independently and its result is reused. The distinction is about data dependency and execution shape, not readability or nesting depth. Modern optimizers often try to decorrelate simple correlated subqueries into joins or semi-joins, but this is not guaranteed, and complex correlated subqueries can become nested-loop-style plans.

## Key points

- A non-correlated nested subquery has no outer reference and can execute once; its result is fed to the outer query.
- A correlated subquery references an outer column, so it is logically evaluated once for each row produced by the outer SELECT, UPDATE, or DELETE.
- Correlated subqueries are common with EXISTS/NOT EXISTS and with comparisons against per-group aggregates, such as max salary within a department.
- If the subquery cannot run standalone as a SELECT, that is a practical sign it is correlated; if it can run standalone, it is non-correlated.
- For many per-group and existence patterns, JOIN/GROUP BY or window functions avoid row-by-row correlation, but the optimizer may already decorrelate simple cases.

## Your 60-second answer

A nested non-correlated subquery is independent: it does not reference the outer query, so the database can run it once and use that result in the outer query. A correlated subquery references at least one column from the outer query, so it is logically evaluated once for each row the outer SELECT, UPDATE, or DELETE processes. For example, `salary > (SELECT AVG(salary) FROM employees)` is non-correlated, while `salary = (SELECT MAX(salary) FROM employees e2 WHERE e2.dept_id = e.dept_id)` is correlated because the inner query uses `e.dept_id`. The main trade-off is performance: literal row-by-row correlation can be expensive on large inputs. Modern engines often decorrelate simple cases into joins, and for the max-per-department pattern a window function is usually cleaner, but I would verify the execution plan rather than trust the syntax alone.

## If they dig deeper

**How do you identify whether a subquery is correlated just by reading the SQL?**

Look for a column reference inside the subquery that is qualified by an alias from a query block outside it. If the inner query has no outer-column reference, it is non-correlated and can be run on its own. If it contains something like `e2.dept_id = e.dept_id` where `e` is from the outer query, it is correlated.

**What is the execution difference between the two on a row-by-row basis?**

A non-correlated subquery is evaluated once, and its result is reused by the outer query. A correlated subquery is conceptually run once for each row from the outer statement, with the current row's values passed into the inner query. The actual plan may differ because optimizers can decorrelate simple cases.

**When is a correlated subquery actually preferable to a JOIN?**

Correlated EXISTS or NOT EXISTS is often clearer for existence checks and can stop at the first matching row for each outer row, which avoids duplicate rows from a join. It also expresses anti-join conditions without returning child rows. If you need columns from the child table, a JOIN is usually more direct.

**How would you rewrite a max-per-department correlated subquery to avoid row-by-row processing?**

Use a window function: `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC)` in a CTE or subquery, then filter where the row number is 1. Alternatively, join to a derived table of `dept_id, MAX(salary)`. Be careful with ties: `ROW_NUMBER` returns one arbitrary row per department unless you add a tie-breaker, while the correlated equality returns all employees tied for the maximum.

**What is query decorrelation, and what can prevent an optimizer from doing it?**

Decorrelation is an optimizer rewrite that converts a correlated subquery into a join, semi-join, or anti-join so the inner query is not re-executed per outer row. PostgreSQL and SQL Server apply such transforms for many simple cases, but limitations appear when the subquery contains side-effecting functions, nondeterministic expressions, outer aggregate references, or complex conditions like LIMIT without ORDER BY. When decorrelation fails, the plan usually becomes a correlated nested loop, so you would check the plan and rewrite manually.

## Worked example

Suppose `employees` has rows: Alice in dept 10 with salary 50k, Bob in dept 10 with 70k, Carol in dept 10 with 90k, Dan in dept 20 with 60k, Erin in dept 20 with 80k. The non-correlated subquery `SELECT name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)` computes AVG = 70k once, then returns Carol and Erin. The correlated version `SELECT name FROM employees e WHERE salary = (SELECT MAX(salary) FROM employees e2 WHERE e2.dept_id = e.dept_id)` is logically run per outer row: for Alice, the inner query gets dept 10 and returns 90k, so she fails; for Carol, 90k equals 90k, so she passes; for Dan, the inner query gets dept 20 and returns 80k, so he fails; Erin passes. The DBMS may decorrelate this into a join against per-department maximums, but the logical dependency remains. A window rewrite with `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC)` and `rn = 1` gives one row per department, while the correlated equality returns all rows tied for the department maximum.

## Common traps

- Saying a subquery is correlated because it is nested; correlation is about referencing outer columns, not depth.
- Assuming the syntax determines the exact execution plan: optimizers may decorrelate correlated subqueries, so row-by-row execution is a logical model, not a physical guarantee.
- Rewriting every correlated query into a JOIN without checking duplicates: a JOIN can multiply rows when the child table has multiple matches, whereas EXISTS does not.
- Forgetting that a max-per-group correlated equality returns all employees tied for the group maximum; if the requirement is one row per group, use a tie-breaker with ROW_NUMBER or handle duplicates explicitly.

</details>

---

### 34. API Gateway · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-api-gateway` then `match: Arrange the following steps in the order an API gateway proc`</sub>

**Question**

Arrange the following steps in the order an API gateway processes a client request, from first to last.

**Options**

A. Route the request to the backend service
B. Enforce rate limits
C. Terminate TLS
D. Authenticate the caller

**Answer (the reader is graded on)**

- before: Terminate TLS → Authenticate the caller · Authenticate the caller → Enforce rate limits · Enforce rate limits → Route the request to the backend service

**Reference answer**

The gateway first terminates TLS to decrypt the request, then authenticates the caller by validating credentials such as a JWT, then enforces rate limits to check quotas, and finally routes the request to the appropriate backend service.

**Graded on**

- TLS termination must happen before any request content can be inspected.
- Authentication identifies the caller before authorization or rate limiting can use the identity.
- Rate limiting uses the authenticated identity to enforce per-client quotas.
- Routing forwards the request to the backend service after all edge policies are applied.

<details><summary>The lesson this came from</summary>

An API gateway is a reverse proxy that accepts all client API calls, applies cross-cutting policies, and forwards each request to the appropriate backend service. In a microservices architecture it hides internal service boundaries behind one client-facing endpoint, handling authentication, authorization, rate limiting, load balancing, caching, request/response transformation, and observability. The gateway itself should contain no business logic; it manages traffic and policy at the edge.

## Why interviewers ask this

At Amazon, Atlassian, Uber, and Patreon, rate-limiter questions probe the same component because gateways are the natural enforcement point. The interviewer is testing whether you can design a single entry point that remains correct under concurrency, scales horizontally, and fails without taking the whole system down. They also look for separation of cross-cutting concerns from business logic.

## The core idea

The gateway is the edge policy engine. It terminates client TLS, authenticates the caller, checks quotas, and then routes the request according to path, method, and headers. It may also compose responses from multiple services or cache them so backend load drops. Because all traffic passes through it, it becomes both the best place to enforce organization-wide rules and the most dangerous single point of failure. A strong design keeps it stateless, horizontally scaled, and equipped with timeouts, retries, and circuit breakers. The routing table or service discovery layer tells it where each request should go without embedding service addresses in clients.

## Key points

- An API gateway terminates client TLS, authenticates requests, authorizes per route, and proxies to backend services, so individual services do not repeat these checks.
- Rate limiting at the gateway can use token bucket or sliding window algorithms; in a distributed deployment the counters must live in a shared store such as Redis rather than per-instance memory.
- API composition lets the gateway call multiple services and merge responses to reduce client round trips, but it adds gateway latency and complexity.
- The gateway must be stateless and horizontally scalable behind a load balancer, with health checks, timeouts, retries, and circuit breakers to avoid cascading failures.
- Common gateway implementations include AWS API Gateway, Kong, and NGINX/OpenResty, though features and configuration models vary by product.

## Your 60-second answer

An API gateway is a single entry point that sits between clients and backend services. It receives every API request, terminates TLS, authenticates the caller, enforces rate limits, and routes the request to the correct service. It also handles cross-cutting concerns like caching, request and response transformation, and monitoring, so downstream services don't duplicate that work. The reason you add one is that microservices expose many fine-grained endpoints; a gateway composes them into one client-friendly API and applies policies at the edge. The main trade-off is that it becomes a critical path: if it fails or is misconfigured, all traffic stops. So you run multiple stateless instances, set timeouts and circuit breakers, and avoid putting business logic in the gateway.

## If they dig deeper

**What are the core responsibilities of an API gateway?**

Routing requests to the correct backend, authentication and authorization, rate limiting, load balancing, caching, request/response transformation, and observability. It can also do API composition, calling multiple services and merging responses. It should not contain business logic.

**How would you implement authentication and authorization at the gateway?**

Validate the caller's credential, usually a JWT or OAuth2 token, at the edge by checking signature, expiry, issuer, and audience. On failure return 401; after authentication check scopes or roles against the route and return 403 if insufficient. Then forward the request with trusted identity headers to downstream services.

**How do you implement rate limiting at the gateway?**

Identify the client by API key, user ID, or IP address. For a single gateway instance, keep a token bucket or sliding window counter in memory; for multiple instances, store counters in Redis with atomic operations. When the limit is exceeded, return HTTP 429 with Retry-After and rate limit headers.

**How do you scale rate limiting across many gateway instances?**

Share the counter state in a central store like Redis and use atomic Lua scripts or sorted sets for sliding windows. Fixed-window counters are simpler but can allow bursts at window boundaries; sliding window log gives accuracy at higher memory cost. If per-instance counters are used, clients can exceed the global limit by hitting different instances, so a shared store is usually required.

**How do you make the gateway fault tolerant and prevent it from becoming a bottleneck?**

Run multiple stateless gateway instances behind a load balancer, set aggressive timeouts, use circuit breakers to stop calling unhealthy services, and retry only idempotent requests. Cache safe responses, monitor CPU and connection saturation, and decide whether to fail open or fail closed when the rate limiter or auth service is unavailable. Keep the gateway free of business logic so changes are rare and deployments are low-risk.

## Worked example

A mobile client sends POST /orders to the gateway. The gateway terminates TLS, validates the JWT signature and expiry, and reads the user ID. It checks a token bucket in Redis for key rate:user:123. The bucket has capacity 100 and refills 10 tokens per second; at this moment 4 tokens remain because the user has consumed 96 requests in the current minute. The gateway allows the request, decrements the bucket to 3, and forwards it to the order service with an X-User-Id header. The order service returns 201, and the gateway strips internal fields before returning JSON. After three more rapid requests the bucket reaches 0, so the next request receives HTTP 429 with Retry-After: 30 and X-RateLimit-Remaining: 0.

## Common traps

- Putting business logic in the gateway, which turns it into a distributed monolith and forces a gateway deployment for every feature change.
- Using per-instance in-memory counters for rate limiting in a multi-instance deployment, allowing a client to exceed the global limit by spreading requests across instances.
- Forgetting timeouts and circuit breakers, so a slow downstream service consumes all gateway threads and makes every API unavailable.
- Assuming the gateway will never fail and not planning redundancy or a fail-open/fail-closed policy, which creates a single point of failure.

</details>

---

## Rank by a metric (`rank-by-metric` · order)

### 35. API Gateway · Medium

*system_design · gate confidence 0.7*

<sub>to object to this card: `## sd-api-gateway` then `match: Rank the following API gateway responsibilities by how much `</sub>

**Question**

Rank the following API gateway responsibilities by how much they increase the gateway's risk of becoming a single point of failure, from highest risk to lowest risk, assuming a standard stateless gateway deployment with no business logic in the gateway.

**Options**

A. Caching responses
B. Routing all traffic through a single entry point
C. Applying rate limiting
D. Enforcing authentication and authorization

**Answer (the reader is graded on)**

- before: Routing all traffic through a single entry point → Enforcing authentication and authorization · Enforcing authentication and authorization → Applying rate limiting · Applying rate limiting → Caching responses

**Reference answer**

The correct order from highest to lowest risk is: routing all traffic through a single entry point, enforcing authentication and authorization, applying rate limiting, and caching responses. Routing all traffic creates the fundamental single point of failure because every request depends on the gateway. Authentication and authorization add a dependency on an external identity provider, so if that service is down or the gateway cannot reach it, requests fail. Rate limiting adds a dependency on a shared state store like Redis; if Redis is unavailable, the gateway may fail open or closed, but the impact is limited to rate limiting. Caching is the least risky because a cache miss or failure simply forwards the request to the backend, so the gateway still functions.

**Graded on**

- Routing all traffic through one entry point is the core single point of failure.
- Authentication and authorization introduce a dependency on an external identity provider.
- Rate limiting in a distributed deployment depends on a shared store such as Redis.
- Caching failures degrade gracefully because requests are forwarded to the backend.

<details><summary>The lesson this came from</summary>

An API gateway is a reverse proxy that accepts all client API calls, applies cross-cutting policies, and forwards each request to the appropriate backend service. In a microservices architecture it hides internal service boundaries behind one client-facing endpoint, handling authentication, authorization, rate limiting, load balancing, caching, request/response transformation, and observability. The gateway itself should contain no business logic; it manages traffic and policy at the edge.

## Why interviewers ask this

At Amazon, Atlassian, Uber, and Patreon, rate-limiter questions probe the same component because gateways are the natural enforcement point. The interviewer is testing whether you can design a single entry point that remains correct under concurrency, scales horizontally, and fails without taking the whole system down. They also look for separation of cross-cutting concerns from business logic.

## The core idea

The gateway is the edge policy engine. It terminates client TLS, authenticates the caller, checks quotas, and then routes the request according to path, method, and headers. It may also compose responses from multiple services or cache them so backend load drops. Because all traffic passes through it, it becomes both the best place to enforce organization-wide rules and the most dangerous single point of failure. A strong design keeps it stateless, horizontally scaled, and equipped with timeouts, retries, and circuit breakers. The routing table or service discovery layer tells it where each request should go without embedding service addresses in clients.

## Key points

- An API gateway terminates client TLS, authenticates requests, authorizes per route, and proxies to backend services, so individual services do not repeat these checks.
- Rate limiting at the gateway can use token bucket or sliding window algorithms; in a distributed deployment the counters must live in a shared store such as Redis rather than per-instance memory.
- API composition lets the gateway call multiple services and merge responses to reduce client round trips, but it adds gateway latency and complexity.
- The gateway must be stateless and horizontally scalable behind a load balancer, with health checks, timeouts, retries, and circuit breakers to avoid cascading failures.
- Common gateway implementations include AWS API Gateway, Kong, and NGINX/OpenResty, though features and configuration models vary by product.

## Your 60-second answer

An API gateway is a single entry point that sits between clients and backend services. It receives every API request, terminates TLS, authenticates the caller, enforces rate limits, and routes the request to the correct service. It also handles cross-cutting concerns like caching, request and response transformation, and monitoring, so downstream services don't duplicate that work. The reason you add one is that microservices expose many fine-grained endpoints; a gateway composes them into one client-friendly API and applies policies at the edge. The main trade-off is that it becomes a critical path: if it fails or is misconfigured, all traffic stops. So you run multiple stateless instances, set timeouts and circuit breakers, and avoid putting business logic in the gateway.

## If they dig deeper

**What are the core responsibilities of an API gateway?**

Routing requests to the correct backend, authentication and authorization, rate limiting, load balancing, caching, request/response transformation, and observability. It can also do API composition, calling multiple services and merging responses. It should not contain business logic.

**How would you implement authentication and authorization at the gateway?**

Validate the caller's credential, usually a JWT or OAuth2 token, at the edge by checking signature, expiry, issuer, and audience. On failure return 401; after authentication check scopes or roles against the route and return 403 if insufficient. Then forward the request with trusted identity headers to downstream services.

**How do you implement rate limiting at the gateway?**

Identify the client by API key, user ID, or IP address. For a single gateway instance, keep a token bucket or sliding window counter in memory; for multiple instances, store counters in Redis with atomic operations. When the limit is exceeded, return HTTP 429 with Retry-After and rate limit headers.

**How do you scale rate limiting across many gateway instances?**

Share the counter state in a central store like Redis and use atomic Lua scripts or sorted sets for sliding windows. Fixed-window counters are simpler but can allow bursts at window boundaries; sliding window log gives accuracy at higher memory cost. If per-instance counters are used, clients can exceed the global limit by hitting different instances, so a shared store is usually required.

**How do you make the gateway fault tolerant and prevent it from becoming a bottleneck?**

Run multiple stateless gateway instances behind a load balancer, set aggressive timeouts, use circuit breakers to stop calling unhealthy services, and retry only idempotent requests. Cache safe responses, monitor CPU and connection saturation, and decide whether to fail open or fail closed when the rate limiter or auth service is unavailable. Keep the gateway free of business logic so changes are rare and deployments are low-risk.

## Worked example

A mobile client sends POST /orders to the gateway. The gateway terminates TLS, validates the JWT signature and expiry, and reads the user ID. It checks a token bucket in Redis for key rate:user:123. The bucket has capacity 100 and refills 10 tokens per second; at this moment 4 tokens remain because the user has consumed 96 requests in the current minute. The gateway allows the request, decrements the bucket to 3, and forwards it to the order service with an X-User-Id header. The order service returns 201, and the gateway strips internal fields before returning JSON. After three more rapid requests the bucket reaches 0, so the next request receives HTTP 429 with Retry-After: 30 and X-RateLimit-Remaining: 0.

## Common traps

- Putting business logic in the gateway, which turns it into a distributed monolith and forces a gateway deployment for every feature change.
- Using per-instance in-memory counters for rate limiting in a multi-instance deployment, allowing a client to exceed the global limit by spreading requests across instances.
- Forgetting timeouts and circuit breakers, so a slow downstream service consumes all gateway threads and makes every API unavailable.
- Assuming the gateway will never fail and not planning redundancy or a fail-open/fail-closed policy, which creates a single point of failure.

</details>

---

### 36. Database sharding · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-database-sharding` then `match: Rank these shard key choices from best to worst for a job sc`</sub>

**Question**

Rank these shard key choices from best to worst for a job scheduler where queries are dominated by per-tenant operations and writes must be evenly distributed across shards.

**Options**

A. status
B. tenant_id
C. due_time
D. user_id

**Answer (the reader is graded on)**

- before: tenant_id → user_id · user_id → due_time · due_time → status

**Reference answer**

The best shard key is tenant_id because it has high cardinality, aligns with the dominant per-tenant access pattern, and spreads writes evenly. user_id is also good but slightly less aligned with tenant-scoped queries. due_time is poor because range sharding on a monotonically increasing timestamp creates write hotspots. status is the worst because it has very low cardinality, causing severe imbalance and hot shards.

**Graded on**

- A good shard key has high cardinality and matches the dominant query pattern.
- tenant_id keeps all jobs for one tenant on a single shard and distributes tenants evenly.
- user_id is high cardinality but may not match tenant-scoped queries as well.
- due_time causes write hotspots when range-sharded, and status has too few distinct values.

<details><summary>The lesson this came from</summary>

Database sharding is horizontal partitioning: a logical table's rows are split into disjoint shards, each stored on a separate database server and holding the same schema. A shard key and routing scheme determine which shard owns a row, so a write or read can be sent directly to the right node. Sharding increases total data capacity and write throughput beyond one machine; it is distinct from replication, which copies the same rows to multiple servers. For MySQL and PostgreSQL, sharding is usually implemented in the application, via a proxy such as Vitess, or through an extension such as Citus; MongoDB has native sharded clusters.

## Why interviewers ask this

Interviewers ask this when a system design grows past a single database. They are testing whether you can choose a shard key from real access patterns, explain how a write or read gets routed, and handle the consequences: hotspots, cross-shard queries, adding capacity, and consistency. Real questions such as designing a job scheduler or a video platform reach sharding at the 'scale across machines' step.

## The core idea

Sharding is a capacity decision, not a default: you partition data only when one server plus replicas can no longer hold the working set or absorb the write load. The shard key determines which queries stay on one shard and which must fan out; choose a high-cardinality key that matches the dominant access pattern. Hash-based routing spreads writes evenly but makes range scans touch every shard; range-based routing keeps ordered scans local but risks writes stacking on one range. Moving shards is expensive, so design rebalancing before launch using consistent hashing, virtual shards, or a directory mapping. Cross-shard joins and transactions are the main recurring cost; real systems often co-locate related rows, denormalize, or aggregate in the application instead.

## Key points

- Sharding splits rows into disjoint shards on separate servers, while replication stores copies of the same rows; a sharded row's primary write goes to exactly one shard.
- A good shard key has high cardinality and aligns with the most common operations; user_id or tenant_id is usually safer than status or country because it spreads data evenly.
- Range-based sharding preserves ordered range scans but can create hotspots on monotonically increasing keys such as timestamps; hash-based sharding spreads load but forces range queries to fan out to all shards.
- Traditional sharded relational databases do not provide cross-shard ACID transactions or joins in the same way a single node does, so you must co-locate, denormalize, or use an application-level join.
- When adding a shard with simple modulo hashing, most keys move; consistent hashing or virtual shards reduce rebalancing to a fraction of keys and are common in distributed systems.

## Your 60-second answer

Sharding is horizontal partitioning: you split a table's rows across multiple database servers by a shard key, so each server holds a subset of the data and the same schema. I'd use it only after a single primary plus read replicas can't hold the data or handle write throughput. The shard key should be high cardinality and match the dominant query pattern—for a job scheduler, tenant_id keeps each tenant's operations on one shard. I'd pick range sharding when ordered scans dominate, hash sharding when I need even distribution, and a directory when I need dynamic movement. The main trade-off is that cross-shard joins and transactions become expensive, so you co-locate related data or aggregate in the application. Rebalancing is the other hard part, so I'd add consistent hashing or virtual shards early.

## If they dig deeper

**How is sharding different from replication?**

Replication keeps full copies of the same data on multiple servers and routes reads to replicas while writes go to the primary. Sharding partitions the data so each row lives on exactly one shard, and different shards handle different subsets. In production you often combine both: each shard may have its own replicas for availability.

**How do you choose a shard key?**

Pick a column that has high cardinality, distributes writes evenly, and appears in most queries. For a job scheduler, tenant_id or user_id keeps all jobs for one tenant on one shard. Avoid low-cardinality keys like status; if you need ordered scans by time but write mostly new rows, range-sharding on timestamp can create a hotspot, so hash may be better.

**What if one shard becomes a hotspot?**

Hotspots usually come from a low-cardinality key or a monotonically increasing range. You can split a hot range into smaller ranges, use a hash with a salt prefix to spread heavy keys, or add virtual shards so hot logical buckets can be moved independently. Monitor keys per shard and rebalance before a node saturates.

**How do you add a new shard without downtime?**

Use consistent hashing or a directory mapping, define the new node's token range, and migrate only the affected key ranges in the background. While migrating, dual-write to old and new shards, verify data with checksums, then atomically update the routing layer to read from the new shard and remove the old copies. Avoid simple modulo because adding a node changes almost every key's target.

**How do you handle cross-shard joins or transactions?**

In many sharded relational databases you can't run a normal SQL join across shards with full ACID, so you either denormalize and co-locate related rows on the same shard, run parallel queries and join in the application, or use a distributed SQL layer that implements cross-shard transactions with a coordinator. If strict consistency is required, look at systems designed for distributed transactions, but this adds latency.

## Worked example

Suppose a job scheduler stores jobs with tenant_id and due_time. With four shards and modulo-4 hashing on tenant_id, tenant 42 maps to shard 2 because 42 % 4 = 2, so all schedule, execute, and history queries for that tenant hit only shard 2. Tenant 43 maps to shard 3. A query for jobs due before 10:00, however, must ask all four shards because due_time is not the shard key. If instead the table is range-sharded by due_time, that query touches only the first range shard, but newly inserted jobs due at the same timestamp pile onto the current hot range. The hash design keeps per-tenant access local; the scheduler can scan each shard independently and merge due jobs.

## Common traps

- Sharding before exhausting a single server, read replicas, and caching, then paying for cross-shard complexity without needing the capacity.
- Picking a low-cardinality shard key like status or region, which creates unbalanced shards and hot nodes.
- Assuming range sharding on an auto-incrementing ID or timestamp is fine; writes concentrate on the highest range and one shard saturates.
- Adding a node by changing a modulo shard count (e.g. 4 to 5) and expecting a small migration; most rows move, requiring large data transfer.

</details>

---

## Timeline (`timeline` · order)

### 37. Service Discovery · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-service-discovery` then `match: Order the steps in the lifecycle of a service instance using`</sub>

**Question**

Order the steps in the lifecycle of a service instance using self-registration with a lease-based registry (e.g., etcd), from the moment the instance starts to the moment it is removed after a crash. Assume the instance crashes without deregistering.

**Options**

A. Instance crashes and stops sending keep-alives
B. Instance starts and registers with the registry
C. Lease expires and the registry deletes the instance's entry
D. Instance sends keep-alives to refresh its lease

**Answer (the reader is graded on)**

- before: Instance starts and registers with the registry → Instance sends keep-alives to refresh its lease · Instance sends keep-alives to refresh its lease → Instance crashes and stops sending keep-alives · Instance crashes and stops sending keep-alives → Lease expires and the registry deletes the instance's entry

**Reference answer**

The correct order is: instance starts and registers with the registry; instance sends keep-alives to refresh its lease; instance crashes and stops sending keep-alives; lease expires and the registry deletes the instance's entry. This reflects the standard self-registration flow with lease-based health tracking: registration establishes the mapping, keep-alives maintain it, and lease expiry is the mechanism that removes a crashed instance.

**Graded on**

- Self-registration: the instance registers itself on startup.
- Lease-based health: the instance must refresh its lease with keep-alives.
- Crash detection: when keep-alives stop, the lease eventually expires.
- Removal: the registry deletes the entry after lease expiry.

<details><summary>The lesson this came from</summary>

Service discovery is the component that lets a client find a live instance of a named service without hardcoded host:port pairs. Instances register with a service registry—Consul, etcd, ZooKeeper, or an orchestration API—and the registry keeps a mapping from service name to current network locations. Discovery can happen client-side, where the client queries the registry and selects an instance, or server-side, where a load balancer queries the registry and routes. Health tracking removes unreachable instances before they receive traffic.

## Why interviewers ask this

In microservices, instances scale, fail, and move; static endpoint configuration breaks under those conditions. Interviewers use service discovery to test whether you can route traffic to ephemeral instances and reason about the health and consistency paths during failure. Large system design problems often assume dynamic service locations, so a weak discovery story undermines the rest of the design.

## The core idea

Service discovery separates the identity of a service from the network location of its instances. A highly available registry stores the mapping from service name to a set of live endpoints; instances register themselves or are registered by an external controller. Health state is maintained either by leases or heartbeats from the instance, or by active checks from the registry. Clients either query the registry directly and load-balance, or delegate routing to a server-side load balancer. The hard part is consistency: a registry can only reflect change as fast as heartbeats, lease expiry, or active checks allow, so there is always a propagation delay after failure.

## Key points

- Client-side discovery has the client query the registry and then call an instance directly; server-side discovery puts a load balancer between clients and instances.
- A service registry must be highly available and up-to-date; common implementations include Consul, etcd, and ZooKeeper.
- Self-registration lets instances register and deregister themselves and send heartbeats; third-party registration uses an external controller or orchestration event to update the registry.
- etcd does not actively poll HTTP health endpoints; it deletes keys when a client-managed lease expires. Consul can perform active health checks.
- There is always a lag between an instance failing and every client stopping traffic to it, bounded by heartbeat or lease TTL plus client cache refresh.

## Your 60-second answer

Service discovery is how a service finds the current network location of another service instance without hardcoded addresses. Each instance registers in a service registry—Consul, etcd, or ZooKeeper—which stores the mapping from service name to live host:port endpoints, and removes entries when instances fail health checks or miss heartbeats. In client-side discovery, the caller queries the registry and selects an instance; in server-side discovery, a load balancer queries the registry and routes the request. Registration can be self-registration by the instance or third-party registration by an orchestrator. The main trade-off is freshness versus availability: a registry can only reflect failure as fast as its TTL or check interval, so clients may briefly call an instance that is already down unless they retry or fall back.

## If they dig deeper

**What is the difference between client-side and server-side discovery?**

In client-side discovery, the client queries the registry, obtains the list of instances, and performs load balancing itself before calling the instance directly. In server-side discovery, the client sends the request to a load balancer or router, which queries the registry and forwards traffic to a chosen instance. Client-side discovery gives clients more control and removes a network hop, but requires a discovery client and load-balancing logic in every service.

**How do instances register themselves, and what are the alternatives?**

Self-registration means the instance calls the registry on startup, deregisters on shutdown, and may send heartbeats. Third-party registration uses an external controller or orchestration platform, such as Kubernetes, to detect containers and update the registry. Self-registration couples the service to the registry; third-party registration centralizes lifecycle awareness but can miss an unhealthy process if the container still exists.

**How does the registry know if an instance is still healthy?**

It depends on the registry. Consul can run active health checks, such as HTTP probes, and mark instances unhealthy after repeated failures. etcd uses client-managed leases: the instance must refresh its lease with keep-alives before TTL expiry, otherwise the key is deleted. ZooKeeper uses ephemeral znodes tied to a session heartbeat. Active checks can test external dependencies; lease expiration only proves the client process can still reach the registry.

**What happens if the service registry itself goes down?**

A strong answer distinguishes the control plane from the data plane. Existing clients may keep using cached endpoints, and server-side load balancers may keep routing from their last known table, so traffic can continue temporarily. New instances cannot register and old ones cannot deregister until the registry recovers, so changes are frozen and failures may not be removed. For this reason the registry is typically run as a small replicated highly available cluster and treated as critical infrastructure.

**How do you avoid a thundering herd of clients querying the registry on every request?**

Clients cache the endpoint list and subscribe to updates or refresh lazily with a bounded TTL or jitter. In server-side discovery, only the load balancer queries the registry, so client fan-out is much smaller. Service meshes push endpoint updates to sidecar proxies through the control plane, avoiding repeated polling. The tradeoff is cache staleness: after a failure, some requests may still target the dead instance until refresh.

## Worked example

Consider a payments service with three instances, each registered under the same service name and sending keep-alives every 3 seconds. The registry lease has a TTL of 10 seconds. A client caches the endpoint list for 30 seconds and load-balances across the instances. If instance B crashes at t=0 and its last keep-alive was at t=0, the registry deletes it when the lease expires at about t=10; before that, the registry still lists B. If the client last refreshed at t=-5, it will keep a cached list containing B until t=25, so it can still call the dead instance. That window is why client-side discovery needs retries or a fallback path, while server-side load balancers can perform active health checks and remove B sooner.

## Common traps

- Assuming every registry actively health-checks instances: etcd uses leases, while Consul supports active HTTP and TCP checks.
- Hardcoding service endpoints in configuration and calling that service discovery: it breaks when instances scale or move.
- Confusing the registry with the load balancer: in client-side discovery, clients query the registry but still call instances directly.
- Forgetting cache staleness: a client with cached endpoints can keep sending traffic to a dead instance after the registry removes it.

</details>

---

### 38. Page Replacement Algorithms · Medium

*cs · gate confidence 0.8*

<sub>to object to this card: `## cs-page-replacement-algorithms` then `match: Arrange the following page replacement algorithms in the ord`</sub>

**Question**

Arrange the following page replacement algorithms in the order they are typically preferred for practical implementation, from most preferred to least preferred, assuming a general-purpose OS where implementation overhead and fault rate both matter.

**Options**

A. FIFO
B. Clock
C. LRU

**Answer (the reader is graded on)**

- before: Clock → LRU · LRU → FIFO

**Reference answer**

Clock is most preferred because it approximates LRU with low overhead. LRU is next because it has good fault rates but exact implementation is expensive. FIFO is least preferred because it is simple but can exhibit Belady's anomaly and generally has worse fault rates.

**Graded on**

- Clock approximates LRU with low overhead, making it the practical choice.
- LRU has good fault rates but requires expensive per-access bookkeeping.
- FIFO is simple but can exhibit Belady's anomaly and generally performs worse.

<details><summary>The lesson this came from</summary>

Page replacement algorithms select which resident page to evict when a page fault occurs and no free frame is available. FIFO evicts the page loaded earliest; LRU evicts the page whose last access is oldest; optimal evicts the page whose next use is farthest in the future; clock approximates LRU using a reference bit and a circular hand. They differ in fault rate, implementation cost, and assumptions about future knowledge.

## Why interviewers ask this

Interviewers test understanding of OS memory management and ability to reason about trade-offs between simplicity, fault rate, and implementation overhead. They also check whether you can implement LRU efficiently and explain anomalies such as Belady's anomaly. It connects to caching, hardware support, and real system design.

## The core idea

Page replacement only matters when memory is full: on a fault, the OS must choose a victim page, and that choice affects the number of future faults. Optimal (OPT) gives the minimum possible faults for a fixed reference string and frame count, but it requires knowing all future references, which a real OS cannot do. Real systems therefore use past behavior: LRU uses the most recent access and has good theoretical properties, but exact LRU needs expensive per-access bookkeeping. Clock keeps one reference bit per frame set by hardware and scans circularly, clearing bits; it approximates LRU with much lower overhead. FIFO is the simplest but can exhibit Belady's anomaly. Practical systems usually choose clock or an enhanced variant.

## Key points

- FIFO evicts the page that has been resident longest, implemented with a queue, and can exhibit Belady's anomaly, where more frames cause more faults for the same reference string.
- LRU evicts the page whose most recent access is oldest and can be implemented in O(1) time with a doubly linked list plus a hash map from page to node.
- Optimal (OPT/MIN) replaces the page whose next use is farthest in the future, producing the minimum possible faults for a given reference string and frame count, but requires future knowledge and is not implementable in practice.
- Clock (second chance) scans a circular buffer of frames, clears reference bits set by hardware on access, and evicts the first frame whose bit is 0; this approximates LRU with very low overhead.
- Enhancing clock with a dirty bit lets the OS prefer evicting clean pages over dirty pages, because writing a dirty page to disk adds I/O cost.

## Your 60-second answer

Page replacement algorithms decide which page to evict when a page fault occurs and no frame is free. FIFO evicts the page that has been in memory longest; it is simple but can suffer Belady's anomaly, where adding frames increases faults. LRU evicts the page whose last access is oldest; it approximates optimal well and has the stack property, but true LRU requires tracking recency on every access, which is expensive in software. Optimal evicts the page whose next use is farthest in the future; it gives the minimum possible faults for a fixed reference string but needs future knowledge, so it cannot be used in a real OS. Clock is the practical compromise: each frame has a hardware-set reference bit, and a hand sweeps circularly, clearing bits and evicting the first page with a zero bit. This approximates LRU with low overhead, so real systems use clock or variants.

## If they dig deeper

**How do you implement an LRU cache efficiently?**

Maintain a doubly linked list ordered from most recently used at the head to least recently used at the tail, and a hash map from page number to list node. On access, move the node to the head; on insertion when full, remove the tail node and its map entry. All operations are O(1).

**What is Belady's anomaly and which algorithms exhibit it?**

It is the counterintuitive case where increasing the number of frames increases the number of page faults for the same reference string. FIFO can exhibit it, while LRU and optimal do not because they are stack algorithms.

**Why can't optimal replacement be used in a real operating system?**

Optimal replacement requires knowing the complete future sequence of page references. A real OS cannot predict future accesses, so it is used offline as a lower bound to evaluate practical algorithms.

**How does clock approximate LRU and why is it preferred over exact LRU?**

Clock keeps one reference bit per frame, which the hardware sets on each access. A circular hand clears bits; a page whose bit is zero has not been used since the hand last passed, so it is evicted. This avoids per-access updates to timestamps or list pointers, making it much cheaper in software while approximating LRU behavior.

**What is enhanced second-chance and how does it handle dirty pages?**

Enhanced second-chance uses both a reference bit and a modify (dirty) bit. It scans frames in a priority order: (reference=0, modify=0) first, then (0,1), then (1,0), then (1,1), preferring clean pages, since evicting a dirty page requires writing it to disk first.

## Worked example

For reference string 1,2,3,4,1,2,5,1,2,3,4,5 with 3 frames, FIFO causes 9 faults, LRU 10, and OPT 7. FIFO trace: after faults on 1,2,3,4, frames are [2,3,4]; then 1 evicts 2, 2 evicts 3, 5 evicts 4; the only hits are on 1 at position 8, 2 at position 9, and 5 at position 12. LRU trace: faults occur at positions 1,2,3,4,5,6,7,10,11,12; at position 10 the LRU page is 5 because 1 and 2 were accessed more recently at positions 8 and 9. OPT trace: at position 4 it evicts 3 because its next use is at 10, farther than 1 at 5 and 2 at 6; at 7 it evicts 4 (next use at 11); at 10 it evicts 1 because it is never used again. OPT has the fewest faults; FIFO beats LRU on this specific trace, showing no algorithm except OPT dominates all others.

## Common traps

- Claiming LRU always faults less than FIFO: on some reference strings FIFO can beat LRU; only OPT is guaranteed minimal.
- Assuming more frames always reduce faults: FIFO can exhibit Belady's anomaly and fault more with more frames.
- Forgetting to update recency on hits in an LRU implementation: if a hit does not move the page to the front, the algorithm behaves more like FIFO.
- Saying optimal can be implemented with machine learning or prediction: OPT requires exact future knowledge; any online predictor is just a heuristic approximation.

</details>

---

## Dependency order (`dependency-order` · order)

### 39. Database sharding · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-database-sharding` then `match: Order the steps for adding a new shard to a sharded database`</sub>

**Question**

Order the steps for adding a new shard to a sharded database without downtime, from first to last.

**Options**

A. Remove the old copies
B. Define the new node's token range
C. Atomically update the routing layer
D. Migrate affected key ranges with dual-writes
E. Verify data with checksums

**Answer (the reader is graded on)**

- before: Define the new node's token range → Migrate affected key ranges with dual-writes · Migrate affected key ranges with dual-writes → Verify data with checksums · Verify data with checksums → Atomically update the routing layer · Atomically update the routing layer → Remove the old copies

**Reference answer**

First, define the new node's token range using consistent hashing or a directory mapping. Then migrate only the affected key ranges in the background while dual-writing to old and new shards. Verify data with checksums, then atomically update the routing layer to read from the new shard. Finally, remove the old copies.

**Graded on**

- Use consistent hashing or a directory mapping to determine which keys move.
- Dual-write during migration keeps both shards consistent.
- Verify with checksums before switching reads.
- Update the routing layer atomically, then clean up old data.

<details><summary>The lesson this came from</summary>

Database sharding is horizontal partitioning: a logical table's rows are split into disjoint shards, each stored on a separate database server and holding the same schema. A shard key and routing scheme determine which shard owns a row, so a write or read can be sent directly to the right node. Sharding increases total data capacity and write throughput beyond one machine; it is distinct from replication, which copies the same rows to multiple servers. For MySQL and PostgreSQL, sharding is usually implemented in the application, via a proxy such as Vitess, or through an extension such as Citus; MongoDB has native sharded clusters.

## Why interviewers ask this

Interviewers ask this when a system design grows past a single database. They are testing whether you can choose a shard key from real access patterns, explain how a write or read gets routed, and handle the consequences: hotspots, cross-shard queries, adding capacity, and consistency. Real questions such as designing a job scheduler or a video platform reach sharding at the 'scale across machines' step.

## The core idea

Sharding is a capacity decision, not a default: you partition data only when one server plus replicas can no longer hold the working set or absorb the write load. The shard key determines which queries stay on one shard and which must fan out; choose a high-cardinality key that matches the dominant access pattern. Hash-based routing spreads writes evenly but makes range scans touch every shard; range-based routing keeps ordered scans local but risks writes stacking on one range. Moving shards is expensive, so design rebalancing before launch using consistent hashing, virtual shards, or a directory mapping. Cross-shard joins and transactions are the main recurring cost; real systems often co-locate related rows, denormalize, or aggregate in the application instead.

## Key points

- Sharding splits rows into disjoint shards on separate servers, while replication stores copies of the same rows; a sharded row's primary write goes to exactly one shard.
- A good shard key has high cardinality and aligns with the most common operations; user_id or tenant_id is usually safer than status or country because it spreads data evenly.
- Range-based sharding preserves ordered range scans but can create hotspots on monotonically increasing keys such as timestamps; hash-based sharding spreads load but forces range queries to fan out to all shards.
- Traditional sharded relational databases do not provide cross-shard ACID transactions or joins in the same way a single node does, so you must co-locate, denormalize, or use an application-level join.
- When adding a shard with simple modulo hashing, most keys move; consistent hashing or virtual shards reduce rebalancing to a fraction of keys and are common in distributed systems.

## Your 60-second answer

Sharding is horizontal partitioning: you split a table's rows across multiple database servers by a shard key, so each server holds a subset of the data and the same schema. I'd use it only after a single primary plus read replicas can't hold the data or handle write throughput. The shard key should be high cardinality and match the dominant query pattern—for a job scheduler, tenant_id keeps each tenant's operations on one shard. I'd pick range sharding when ordered scans dominate, hash sharding when I need even distribution, and a directory when I need dynamic movement. The main trade-off is that cross-shard joins and transactions become expensive, so you co-locate related data or aggregate in the application. Rebalancing is the other hard part, so I'd add consistent hashing or virtual shards early.

## If they dig deeper

**How is sharding different from replication?**

Replication keeps full copies of the same data on multiple servers and routes reads to replicas while writes go to the primary. Sharding partitions the data so each row lives on exactly one shard, and different shards handle different subsets. In production you often combine both: each shard may have its own replicas for availability.

**How do you choose a shard key?**

Pick a column that has high cardinality, distributes writes evenly, and appears in most queries. For a job scheduler, tenant_id or user_id keeps all jobs for one tenant on one shard. Avoid low-cardinality keys like status; if you need ordered scans by time but write mostly new rows, range-sharding on timestamp can create a hotspot, so hash may be better.

**What if one shard becomes a hotspot?**

Hotspots usually come from a low-cardinality key or a monotonically increasing range. You can split a hot range into smaller ranges, use a hash with a salt prefix to spread heavy keys, or add virtual shards so hot logical buckets can be moved independently. Monitor keys per shard and rebalance before a node saturates.

**How do you add a new shard without downtime?**

Use consistent hashing or a directory mapping, define the new node's token range, and migrate only the affected key ranges in the background. While migrating, dual-write to old and new shards, verify data with checksums, then atomically update the routing layer to read from the new shard and remove the old copies. Avoid simple modulo because adding a node changes almost every key's target.

**How do you handle cross-shard joins or transactions?**

In many sharded relational databases you can't run a normal SQL join across shards with full ACID, so you either denormalize and co-locate related rows on the same shard, run parallel queries and join in the application, or use a distributed SQL layer that implements cross-shard transactions with a coordinator. If strict consistency is required, look at systems designed for distributed transactions, but this adds latency.

## Worked example

Suppose a job scheduler stores jobs with tenant_id and due_time. With four shards and modulo-4 hashing on tenant_id, tenant 42 maps to shard 2 because 42 % 4 = 2, so all schedule, execute, and history queries for that tenant hit only shard 2. Tenant 43 maps to shard 3. A query for jobs due before 10:00, however, must ask all four shards because due_time is not the shard key. If instead the table is range-sharded by due_time, that query touches only the first range shard, but newly inserted jobs due at the same timestamp pile onto the current hot range. The hash design keeps per-tenant access local; the scheduler can scan each shard independently and merge due jobs.

## Common traps

- Sharding before exhausting a single server, read replicas, and caching, then paying for cross-shard complexity without needing the capacity.
- Picking a low-cardinality shard key like status or region, which creates unbalanced shards and hot nodes.
- Assuming range sharding on an auto-incrementing ID or timestamp is fine; writes concentrate on the highest range and one shard saturates.
- Adding a node by changing a modulo shard count (e.g. 4 to 5) and expecting a small migration; most rows move, requiring large data transfer.

</details>

---

### 40. Indexes · Easy

*sql · gate confidence 0.8*

<sub>to object to this card: `## sql-indexes` then `match: Arrange the following steps in the order a database engine p`</sub>

**Question**

Arrange the following steps in the order a database engine performs them when executing a query that uses a composite index on (a, b, c) with WHERE a = 1 AND b > 2 AND c = 3, assuming index condition pushdown is available.

**Options**

A. Apply c = 3 as a residual predicate on scanned index entries
B. Scan the contiguous range of index entries where b > 2
C. Seek to the first index entry matching a = 1

**Answer (the reader is graded on)**

- before: Seek to the first index entry matching a = 1 → Scan the contiguous range of index entries where b > 2 · Scan the contiguous range of index entries where b > 2 → Apply c = 3 as a residual predicate on scanned index entries

**Reference answer**

The engine first seeks to the first index entry matching a = 1, then scans the contiguous range of entries where b > 2, and finally applies the residual predicate c = 3 to each scanned index entry before performing any base table lookups.

**Graded on**

- Equality on the leading column a positions the seek.
- Range on b bounds the scan within the a = 1 group.
- c is applied as a filter during the index scan, not as part of the seek range.

<details><summary>The lesson this came from</summary>

An index is a separate data structure, usually a B-tree, that stores a sorted copy of one or more columns from a database table plus a pointer to the row the values came from. It lets the query planner seek or range-scan on key columns instead of scanning the entire table. Engines differ in clustering: SQL Server has one clustered index that determines physical row order and non-clustered indexes as separate B-trees; MySQL InnoDB always clusters by the primary key; PostgreSQL stores table rows in an unordered heap and all standard indexes are secondary.

## Why interviewers ask this

Interviewers use indexes to test whether you understand real database performance, not just syntax. They want to see you can choose a good index for a given query, reason about composite key order and covering indexes, and explain the write/storage tradeoff. Many candidates can recite CREATE INDEX but cannot predict when an index helps or hurts.

## The core idea

An index is a copy of data organized for search: it speeds up reads because the engine can walk a B-tree instead of scanning every row, but it adds storage and every insert/update/delete must keep the copies in sync. Composite indexes work left-to-right: equality columns position the seek, a range column bounds the scan, and later columns cannot narrow the seek range but can still be applied as predicates inside the index scan before row lookups in engines that support index condition pushdown. Write cost is engine-dependent: in PostgreSQL's append-only MVCC, an UPDATE creates a new tuple version and unless HOT optimization applies, all secondary indexes on the table receive entries for the new version, even when no indexed column changed.

## Key points

- Most general-purpose SQL indexes are B-trees that support O(log n + rows returned) seeks and range scans, compared with O(n) full table scans.
- A composite index on (a, b, c) can only be used efficiently for lookups that include leading columns; a query filtering only on b or c usually cannot use that index for a seek.
- For a WHERE clause with equality on a and range on b, c cannot narrow the seek range, but engines such as MySQL, SQL Server, PostgreSQL and Oracle can still apply c as an index filter while scanning the index.
- In SQL Server, clustered indexes define physical row order and are limited to one per table; MySQL InnoDB always has a clustered primary key; PostgreSQL has no clustered indexes and stores rows in a heap with secondary indexes pointing to row locations.
- In PostgreSQL's MVCC, an UPDATE writes a new tuple version and, unless HOT is possible on the same page, all secondary indexes are updated to point to the new version even if the updated columns are not part of any index.

## Your 60-second answer

A database index is a separate data structure, typically a B-tree, that keeps a sorted copy of one or more columns and pointers to the corresponding rows. It lets the optimizer find rows by seeking or scanning a small range instead of reading the whole table. In exchange, indexes consume storage and write operations must keep them in sync, so write-heavy tables can slow down significantly. How the columns are ordered matters: for a composite index, equality columns must come before range columns, and any column after the range cannot narrow the seek but can still be applied as a filter during the index scan in modern engines. Clustered indexes, where supported, define the table's physical order; non-clustered indexes are separate structures.

## If they dig deeper

**What are the main costs of creating too many indexes?**

Each index duplicates the key columns and adds storage. Writes must update indexes, increasing insert/update/delete latency. In MVCC engines like PostgreSQL, even updating a non-indexed column can force writes to every secondary index unless HOT optimization is possible on the same page.

**Given an index on (a, b, c) and WHERE a = 1 AND b > 2 AND c = 3, how much of the index is used?**

The B-tree can use a as an equality seek and then range scan b > 2. C cannot narrow the start or end of that b range because the index is sorted first by a, then b, so c values are not consecutive for all b > 2. Modern engines such as MySQL, SQL Server, PostgreSQL and Oracle still apply c as a residual predicate inside the index scan, avoiding base table lookups for rows that fail c = 3.

**Explain the difference between clustered and non-clustered indexes.**

A clustered index determines the physical order of table rows; SQL Server allows at most one per table and the leaf level is the data pages. MySQL InnoDB always stores rows in the primary key's clustered B-tree, with secondary indexes holding primary key values to find rows. PostgreSQL has no clustered index concept in its normal storage: rows live in an unordered heap, and every index, including the primary key, is a secondary structure pointing to row locations.

**Why does PostgreSQL update every secondary index when you change a non-indexed column?**

PostgreSQL uses MVCC: an UPDATE does not overwrite the old row, it writes a new physical tuple version. Every secondary index entry points to the physical tuple location, so the database must add entries for the new version into all indexes on the table. The HOT optimization avoids this only when the new tuple fits on the same heap page and no indexed column changes; then old index entries can be redirected via the line pointer, so secondary indexes remain unchanged.

## Worked example

Take an orders table with columns customer_id, order_date, status, and amount, and an index on (customer_id, order_date, status). A query asks: SELECT * FROM orders WHERE customer_id = 42 AND order_date BETWEEN '2024-01-01' AND '2024-06-30' AND status = 'shipped'. The B-tree descends to customer_id 42, then scans the order_date range as a contiguous block. Because the next key column status comes after order_date, it cannot start the scan at the first 'shipped' row inside that range; the scan visits all rows with order_date in that range. With index condition pushdown, the engine evaluates status = 'shipped' on the index entries and only performs base table lookups for rows that pass, avoiding I/O for rows that do not match. Without ICP, every row in the order_date range would trigger a lookup to check status.

## Common traps

- Believing an index on (a,b,c) can speed up a query that filters only on b or c; without leading column a, the B-tree cannot provide a direct seek.
- Over-indexing because each index helps a read; on a write-heavy table, the accumulated index maintenance can dominate and even hurt overall workload.
- Assuming 'c' is useless after a range on 'b' in a composite index; it cannot narrow the seek range but can still be used as an index filter before table access.
- Confusing clustered with unique: a clustered index concerns physical storage order, while a unique index is a constraint that rejects duplicate key values.

</details>

---

## Interleaving (`interleaving` · order)

### 41. Lambda expressions · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-lambda-expressions` then `match: Order the steps the Java compiler and runtime take when a la`</sub>

**Question**

Order the steps the Java compiler and runtime take when a lambda expression is used, from the moment the source code is compiled to the moment the lambda can be invoked. Assume a standard Java 8+ compiler and runtime.

**Options**

A. The LambdaMetafactory generates or returns a class implementing the functional interface.
B. The compiler emits an invokedynamic call site with a method handle to a synthetic method.
C. The lambda can be invoked through the generated instance.
D. The compiler checks that the target type is a functional interface.

**Answer (the reader is graded on)**

- before: The compiler checks that the target type is a functional interface. → The compiler emits an invokedynamic call site with a method handle to a synthetic method. · The compiler emits an invokedynamic call site with a method handle to a synthetic method. → The LambdaMetafactory generates or returns a class implementing the functional interface. · The LambdaMetafactory generates or returns a class implementing the functional interface. → The lambda can be invoked through the generated instance.

**Reference answer**

The compiler first checks that the lambda's target type is a functional interface, then emits an invokedynamic call site with a method handle to a synthetic method containing the lambda body. At runtime, the LambdaMetafactory uses that method handle to generate or return a class implementing the functional interface, and finally the lambda can be invoked through that instance.

**Graded on**

- Target typing happens at compile time: the lambda must be assigned to a functional interface.
- The compiler emits invokedynamic with a method handle to a synthetic private method.
- At runtime, LambdaMetafactory creates or returns an implementation of the functional interface.
- The lambda is then invoked through the generated instance.

<details><summary>The lesson this came from</summary>

A lambda expression is a syntactic construct that creates an instance of a functional interface by supplying the body of its single abstract method inline. The arrow operator separates an optional parameter list from a body, which can be a single expression or a block. Lambda expressions were introduced in Java 8 as a concise alternative to anonymous classes that implement exactly one method.

## Why interviewers ask this

Interviewers ask about lambdas to check whether you understand Java 8's shift toward passing behavior as data and how lambdas relate to functional interfaces. They probe target typing, capture rules, and the common java.util.function interfaces because those feed directly into streams and collection pipelines.

## The core idea

In Java, a lambda expression is the body of the one abstract method in a target functional interface. The compiler uses the expected type from the assignment, cast, or method argument to infer parameter types and check return compatibility. A lambda can capture local variables only if they are effectively final—never reassigned anywhere in their scope—but it can always read and modify instance fields and static fields. At runtime, the JVM uses invokedynamic and the LambdaMetafactory to create the call site rather than generating a separate anonymous class file at compile time. A lambda body may be a single expression whose value is returned automatically, or a block with explicit returns and statements.

## Key points

- A lambda expression always implements a functional interface, which has exactly one abstract method; default and static methods do not count toward that one.
- Target typing determines the lambda's type from the surrounding context—assignment, cast, or method argument—not from the lambda's own body.
- Parameter types may be omitted, a single untyped parameter may drop parentheses, and the body can be an expression returning a value or a block with statements and explicit returns.
- Captured local variables must be effectively final, meaning they are never reassigned anywhere in their scope, while instance fields and static variables may be read and modified freely.
- Common functional interfaces include Predicate<T> with boolean test(T), Function<T,R> with R apply(T), Consumer<T> with void accept(T), and Supplier<T> with T get().

## Your 60-second answer

A lambda expression is Java's concise syntax for implementing a functional interface inline. You write the parameter list, an arrow, and a body, and the compiler treats that as providing the single abstract method of whatever functional interface is expected at that spot. For example, `Runnable r = () -> System.out.println(42);` creates a Runnable without the boilerplate of an anonymous class. Lambdas matter because they let you pass behavior as data to methods like `forEach`, `filter`, and `map`, especially with the Streams API added in Java 8. One trade-off is that they can only target interfaces with exactly one abstract method, so if you need to implement two methods you still write an anonymous class. Another trade-off is captured local variables must be effectively final, which sometimes forces a workaround like using a single-element array or a field.

## If they dig deeper

**What is a functional interface, and how does @FunctionalInterface work?**

A functional interface is an interface with exactly one abstract method. Default and static methods do not count toward that one. The @FunctionalInterface annotation is optional but when present it makes the compiler fail if the interface has zero or more than one abstract method.

**Can you assign a lambda to Object or use var with it? Why not?**

No. A lambda expression needs a target type that is a functional interface because it supplies the body of that interface's single abstract method. Object has no abstract method, so the compiler cannot infer a functional interface; you need a cast like `(Runnable) () -> ...` or an explicit functional interface target such as a variable declaration.

**What are the rules for capturing variables in a lambda expression?**

Local variables and parameters from the enclosing method can be read only if they are effectively final—never reassigned anywhere in their scope. Instance fields and static fields can always be read and modified. A lambda cannot access default methods of the functional interface it implements because there is no interface instance `this` available inside the lambda.

**How does the JVM implement lambdas differently from anonymous inner classes?**

At compile time, the compiler emits an invokedynamic call site with a method handle to a synthetic private method containing the lambda body. At runtime, the LambdaMetafactory uses that method handle to generate or return a class implementing the functional interface; no separate class file is created for each lambda, unlike anonymous inner classes which generate a distinct class at compile time.

**What are the scoping differences between a lambda and an anonymous inner class?**

A lambda is lexically scoped: `this` and `super` refer to the enclosing instance, not the lambda object, and a lambda parameter cannot shadow a local variable from the enclosing method. An anonymous inner class has its own `this`, and its parameters and locals can shadow enclosing variables because it introduces a new nested scope.

## Worked example

Take `List<String> words = Arrays.asList("apple", "pear", "kiwi");` and the call `Collections.sort(words, (a, b) -> a.length() - b.length());`. The second argument's expected type is `Comparator<String>`, whose `compare` method takes two `String` parameters and returns `int`, so the compiler infers `a` and `b` as `String` and accepts the expression body as the returned difference. If you tried to assign that same lambda to a `Function<String, Integer>`—a one-parameter interface—the parameter count mismatches and compilation fails even though an int is returned. For capturing, `int limit = 5; List<Integer> xs = Arrays.asList(1, 2, 3); xs.replaceAll(x -> x * limit);` compiles because `limit` is never reassigned; adding `limit = 6` anywhere in the method makes `limit` not effectively final and the lambda will not compile. These two examples show target typing and effective final capture.

## Common traps

- Assigning a lambda to Object or using var without a functional interface target: compilation fails because a lambda has no independent type.
- Thinking a captured local variable can be reassigned as long as the reassignment happens before the lambda: any reassignment in scope breaks effective finality, even before the lambda is created.
- Conflating lambda with anonymous inner class for `this`: inside a lambda `this` is the enclosing object, not the lambda instance.
- Using a zero-argument lambda as a Consumer: Consumer's accept method takes one argument, so `() -> list.add(x)` targets a zero-argument void interface such as Runnable, not Consumer.

</details>

---

### 42. ArrayList vs LinkedList · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-arraylist-vs-linkedlist` then `match: Order the following operations by their worst-case time comp`</sub>

**Question**

Order the following operations by their worst-case time complexity for a LinkedList with n elements, from fastest to slowest. Assume standard implementations and no iterator is already positioned at the target node.

**Options**

A. get(n/2)
B. removeFirst
C. add(0, x)
D. get(0)

**Answer (the reader is graded on)**

- before: removeFirst → get(0) · get(0) → add(0, x) · add(0, x) → get(n/2)

**Reference answer**

The correct order is: removeFirst, get(0), add(0, x), get(n/2). removeFirst unlinks the head node in O(1). get(0) returns the head item in O(1). add(0, x) links a new node at the head in O(1). get(n/2) traverses from the nearer end, taking O(n) time.

**Graded on**

- removeFirst and add(0, x) are O(1) because they only update the head pointer.
- get(0) is O(1) because the head node is directly accessible.
- get(n/2) is O(n) because it must follow links from the closer end.

<details><summary>The lesson this came from</summary>

ArrayList stores elements in a contiguous, dynamically resized array; an index read computes a direct memory offset from the base reference. LinkedList stores each element in a separate node carrying item, previous, and next references, so there is no contiguous layout and reaching an index requires following links from the closest end. Both implement List and preserve insertion order; LinkedList additionally implements Deque. Neither class synchronizes its methods.

## Why interviewers ask this

Interviewers ask this to see whether you choose a structure from actual access patterns rather than repeating a table. They test the nuance that 'LinkedList is faster for insert/delete' is only true at the ends or once a node/iterator is positioned, not at an arbitrary index; they also look for understanding of cache locality, memory overhead, and amortized analysis.

## The core idea

The decision comes from memory layout. ArrayList gives O(1) indexed reads and writes because array indexes are offset calculations, and iteration is cache-friendly because elements are adjacent. LinkedList gives O(1) link/unlink for addFirst/addLast/removeFirst/removeLast and for iterator.remove() because the node is already located; inserting at an arbitrary position still costs an O(n) traversal to find that node. At an arbitrary index, both have O(n) cost - ArrayList shifts references, LinkedList follows pointers - so LinkedList has no asymptotic advantage there. Appending to ArrayList is amortized O(1), though growth occasionally copies the array. LinkedList has more per-element memory overhead due to prev/next references, while ArrayList can waste space in unused capacity.

## Key points

- ArrayList is backed by one resizable object array; LinkedList is a doubly linked list of nodes with prev and next references.
- get(int) is O(1) for ArrayList and O(n) for LinkedList because LinkedList traverses from the nearer end.
- Adding or removing at the ends is O(1) for LinkedList; adding at the end is amortized O(1) for ArrayList but occasionally triggers a resize and copy.
- Adding or removing at an arbitrary index is O(n) for both lists: ArrayList shifts elements, LinkedList traverses to the position.
- ArrayList has better cache locality and lower per-element overhead, while LinkedList implements both List and Deque, making it usable as a queue or stack.

## Your 60-second answer

ArrayList is backed by a resizable array; LinkedList is a doubly linked list of nodes. That difference drives the performance. Indexed access is O(1) in ArrayList because get(i) reads a direct array offset. LinkedList get(i) is O(n), walking from the closer end. Insertion and deletion are subtler. Adding or removing at the head or tail of a LinkedList is O(1), which is why its Deque methods are efficient. Adding to the end of an ArrayList is amortized O(1), with an occasional resize copy. At a middle index, both are O(n): ArrayList shifts elements, LinkedList traverses to the node and then links/unlinks. In practice ArrayList usually wins for iteration and random access due cache locality; I default to ArrayList, and pick LinkedList only when the workload is dominated by adding or removing at the ends.

## If they dig deeper

**When would you choose LinkedList instead of ArrayList?**

I would choose LinkedList when the dominating operations are addFirst, removeFirst, addLast, or removeLast - Deque-style work - and random get(i) or heavy iteration is rare. If a queue or stack is needed, I compare it to ArrayDeque: ArrayDeque usually has lower memory overhead and better cache behavior, so I would pick LinkedList mainly when I also need List methods, indexed access in rare cases, or null elements.

**Is LinkedList actually faster for insertion and deletion than ArrayList?**

Only at the ends or through an iterator that already has the node. At an arbitrary index, LinkedList first traverses O(n) to reach the position, then unlinks/links in O(1), so the total is O(n), just like ArrayList's shift. For small or medium list sizes, ArrayList's contiguous copying can beat LinkedList's pointer chasing because of cache locality, so 'LinkedList is faster' is not a universal rule.

**What is the RandomAccess marker interface and how is it used?**

RandomAccess is an empty interface that ArrayList implements and LinkedList does not. JDK algorithms such as Collections.binarySearch and Collections.shuffle check list instanceof RandomAccess; if true they use indexed get/set, otherwise they switch to iterator-based or array-based strategies to avoid accidental O(n^2) behavior on sequential lists.

**How does ArrayList growth work, and why does initial capacity matter?**

In OpenJDK, an ArrayList created with no arguments uses an initial capacity of 10 on first add. When adding would exceed capacity, it allocates a new array about 1.5 times the old length and copies existing references. If the approximate final size is known, supplying an initial capacity avoids repeated allocations; trimToSize can shrink the backing array to the current size.

**What is the complexity of iterator.remove() in ArrayList versus LinkedList, and why?**

ArrayList's iterator.remove() is O(n) because after deleting the element at the cursor, every later reference must be shifted left in the backing array. LinkedList's iterator.remove() is O(1) because the iterator already holds a reference to the current node, so the implementation just unlinks that node by updating its neighbors' prev/next fields.

## Worked example

Consider two lists each holding 100,000 Integer references. `a.get(50_000)` on ArrayList reads one array slot in O(1); `l.get(50_000)` on LinkedList starts at the closer end and follows 50,000 links, O(n). `a.add(0, x)` shifts all 100,000 existing references one slot to the right, O(n); `l.add(0, x)` only allocates a node and updates the head pointer, O(1). `a.add(50_000, x)` shifts 50,000 references; `l.add(50_000, x)` walks 50,000 links then links the node, so both are O(n). The asymmetry is position, not operation name.

## Common traps

- Believing LinkedList is faster than ArrayList for all insertions and deletions; at an arbitrary index it still requires O(n) traversal, and ArrayList's shift can be cheaper due to cache locality.
- Using an indexed for loop with LinkedList because of get(i); repeated get(i) from each iteration causes O(n^2) traversal, while an iterator is O(n).
- Ignoring the RandomAccess marker and choosing algorithms without it; algorithms may degrade on sequential lists.
- Assuming ArrayList end insertion is O(1) worst-case; it is amortized O(1) because resize copies the whole array occasionally.

</details>

---

## Term meaning (`term-meaning` · match)

### 43. Deadlocks · Hard

*cs · gate confidence 0.8*

<sub>to object to this card: `## cs-deadlocks` then `match: Match each deadlock-related term with its correct definition`</sub>

**Question**

Match each deadlock-related term with its correct definition.

**Options**

**Left**: Mutual exclusion, Hold-and-wait, No preemption, Circular wait
**Right**: A resource cannot be forcibly taken away; it is released only voluntarily., A process holds some resources while waiting for others., A closed chain of processes in which each waits for a resource held by the next., A resource cannot be shared and is held by only one process at a time.

**Answer (the reader is graded on)**

- 0 ↔ 3 · 1 ↔ 1 · 2 ↔ 0 · 3 ↔ 2

**Why (right answer, wrong reason is wrong)**

→ **A. Because a cycle in the wait-for graph means each process is waiting for a resource held by another process in the cycle, so none can proceed.**
  B. Because circular wait is the only condition that involves multiple processes, while the others involve a single process.
  C. Because circular wait is the condition that is easiest to break by imposing a global lock order.
  D. Because circular wait is the condition that is detected by the Banker's algorithm.

**Reference answer**

The correct matches are: Mutual exclusion — a resource cannot be shared and is held by only one process at a time; Hold-and-wait — a process holds some resources while waiting for others; No preemption — a resource cannot be forcibly taken away, only released voluntarily; Circular wait — a closed chain of processes where each waits for a resource held by the next. These are the four Coffman conditions that must all hold simultaneously for a deadlock to occur.

**Graded on**

- All four Coffman conditions must hold simultaneously for a deadlock.
- Mutual exclusion means a resource is non-shareable.
- Hold-and-wait means a process holds resources while requesting more.
- Circular wait is a cycle in the wait-for graph.

<details><summary>The lesson this came from</summary>

A deadlock is a circular wait among processes or transactions where each holds a resource and waits for a resource held by another member of the cycle, so none can progress. It occurs only when all four Coffman conditions hold at once: mutual exclusion, hold-and-wait, no preemption, and circular wait. Systems handle deadlocks by prevention, avoidance, or detection and recovery. Prevention makes one condition impossible, avoidance grants requests only if the resulting state is safe, and detection lets cycles form then aborts victims.

## Why interviewers ask this

Interviewers ask about deadlocks to test whether you can reason about concurrent resource acquisition, not just recite definitions. They want to see you identify a circular wait in a concrete locking order and choose among prevention, avoidance, and detection based on the system's constraints. A strong answer explains the tradeoffs: prevention is predictable but conservative, detection enables more concurrency but has unpredictable rollbacks.

## The core idea

Deadlock is ultimately a cycle in the wait-for relationship: each participant holds something another waits for. You can attack it by making one of the four required conditions impossible, such as imposing a global lock order to break circular wait. Avoidance, like Banker's algorithm, allows the conditions to exist but refuses requests that could lead to an unsafe state. Detection lets cycles occur and then breaks them by terminating or rolling back at least one participant. The central tradeoff is concurrency versus predictability: prevention and avoidance reduce concurrency to avoid deadlocks, while detection preserves concurrency but accepts runtime aborts.

## Key points

- All four Coffman conditions—mutual exclusion, hold-and-wait, no preemption, and circular wait—must hold simultaneously for a deadlock; breaking any one prevents it.
- Acquiring locks in a globally consistent order is the most common way to break circular wait in practice.
- Banker's algorithm avoids deadlock by only granting a request if the resulting state remains safe, but it requires each process's maximum resource demand in advance.
- A cycle in a resource allocation graph always means deadlock only when each resource type has a single instance; with multiple instances, a cycle is necessary but not sufficient.
- Recovery selects victims by cost criteria such as priority, work done, or resources held; database transactions can roll back, while OS processes may be killed.

## Your 60-second answer

A deadlock is a circular wait where each process or transaction holds a resource another participant needs, so no one makes progress. It requires all four Coffman conditions to hold: mutual exclusion, hold-and-wait, no preemption, and circular wait. To handle it, you can prevent deadlock by making one condition impossible—usually by imposing a global lock order to break circular wait—or avoid it dynamically, as in Banker's algorithm, by granting a request only if the resulting state is safe. Alternatively, you can allow deadlocks, detect the circular wait, and recover by terminating or rolling back a victim. Prevention is simple and predictable; avoidance requires maximum resource demands; detection keeps concurrency higher but adds overhead and causes unpredictable aborts.

## If they dig deeper

**What are the four Coffman conditions required for deadlock?**

Mutual exclusion: a resource cannot be shared. Hold-and-wait: a process holds some resources while waiting for others. No preemption: a resource cannot be forcibly taken away; it is released only voluntarily. Circular wait: there is a closed chain of processes in which each waits for a resource held by the next. All four must be present at once.

**How do you prevent deadlock in code that acquires multiple locks?**

Enforce a global order on lock acquisition, such as by lock address or priority, so no two threads can hold locks in opposite order and form a cycle. If ordering is not possible, try-lock with timeouts and release all held locks on failure can break hold-and-wait. Avoiding nested locks where possible is also effective.

**Does a cycle in a resource allocation graph always indicate a deadlock?**

Only when every resource type has one instance; then each cycle is an actual permanent circular wait. With multiple instances, a cycle is necessary but not sufficient: a process in the cycle may still complete using another available instance. In that case you need a graph-reduction algorithm or Banker's-style safe-state check.

**Walk through how the Banker's algorithm decides whether a state is safe.**

Start with Work equal to Available. Repeatedly find an unfinished process whose remaining Need is less than or equal to Work, mark it finished, and add its Allocation to Work as if it released its resources. If all processes can be finished in some order, the state is safe. A request is granted only if simulating the grant leaves the system in a safe state; otherwise the requester must wait.

**Why do production databases typically use deadlock detection and rollback instead of Banker's avoidance?**

Banker's algorithm requires knowing each transaction's maximum lock demand in advance, which is impractical for ad hoc queries and dynamic workloads. Databases already track lock wait-for relationships, so they can detect a cycle and abort one transaction. For example, MySQL InnoDB detects row/table lock deadlocks and rolls back one transaction; PostgreSQL also aborts a waiting transaction on detection. This preserves more concurrency than prevention while accepting occasional rollbacks.

## Worked example

Consider a system with three resource types A, B, C and Available=(3,3,2). Five processes have allocations P0=(0,1,0), P1=(2,0,0), P2=(3,0,2), P3=(2,1,1), P4=(0,0,2) and maximum demands P0=(7,5,3), P1=(3,2,2), P2=(9,0,2), P3=(2,2,2), P4=(4,3,3). Need is max minus allocation, so P1 needs (1,2,2) and P3 needs (0,1,1). The state is safe: run P1 first, releasing (2,0,0) to make Work=(5,3,2); then P3 makes Work=(7,4,3); then P4, P0, and finally P2. Now suppose P2 requests (3,0,0). That request does not exceed its need of (6,0,0) or the available A=3, so it would be tentatively granted: available becomes (0,3,2), P2's allocation becomes (6,0,2), and P2's remaining need becomes (3,0,0). In the resulting state, only P3 can finish, after which Work=(2,4,3), but no remaining process has need ≤ Work, so the state is unsafe. Banker's algorithm therefore denies the request and leaves P2 waiting.

## Common traps

- Claiming that a cycle in a resource allocation graph always means deadlock even when resource types have multiple instances; a cycle is necessary but not sufficient in that case.
- Saying Banker's algorithm is commonly used in real operating systems, when it actually requires advance maximum resource claims and is mostly a conceptual avoidance algorithm.
- Confusing prevention with avoidance: prevention statically breaks a Coffman condition, while avoidance lets all four exist but dynamically refuses unsafe grants.
- Forgetting that breaking hold-and-wait by acquiring all resources upfront can sharply reduce concurrency and may cause starvation or indefinite waiting.

</details>

---

### 44. Exceptions · Hard

*java · gate confidence 0.8*

<sub>to object to this card: `## java-exceptions` then `match: Match each Java exception-related term with its meaning. Ass`</sub>

**Question**

Match each Java exception-related term with its meaning. Assume standard Java semantics.

**Options**

**Left**: Checked exception, Unchecked exception, try-with-resources, finally, Suppressed exception
**Right**: A block that always executes after try/catch, even if an exception is thrown, An exception attached to a primary exception, typically from resource closure failure, A construct that automatically closes AutoCloseable resources in reverse declaration order, Exception subclasses excluding RuntimeException that must be caught or declared, RuntimeException and Error, which require no compile-time handling

**Answer (the reader is graded on)**

- 0 ↔ 3 · 1 ↔ 4 · 2 ↔ 2 · 3 ↔ 0 · 4 ↔ 1

**Why (right answer, wrong reason is wrong)**

→ **A. Because the compiler enforces handling only for exceptions that represent expected, recoverable conditions, while programming bugs and JVM failures are not forced to be caught.**
  B. Because checked exceptions are all subclasses of Throwable, and the compiler requires handling for every Throwable subtype.
  C. Because unchecked exceptions are only those thrown by the JVM itself, not by application code.
  D. Because try-with-resources is the only way to close resources, so checked exceptions must be declared to use it.

**Reference answer**

Checked exceptions are Exception subclasses excluding RuntimeException and must be caught or declared. Unchecked exceptions are RuntimeException and Error, requiring no compile-time handling. try-with-resources automatically closes AutoCloseable resources in reverse declaration order. finally always executes after try/catch, even if an exception is thrown. Suppressed exceptions are secondary exceptions attached to a primary exception, typically from resource closure failures.

**Graded on**

- Checked exceptions must be caught or declared; unchecked exceptions are not enforced.
- try-with-resources closes resources in reverse declaration order and suppresses close failures.
- finally runs regardless of whether an exception is thrown.
- Suppressed exceptions preserve secondary failures without losing the primary exception.

<details><summary>The lesson this came from</summary>

Java exception handling is the structured mechanism for throwing and catching java.lang.Throwable subclasses so control transfers from the point of failure to code that can recover or fail cleanly. Throwable has two primary subclasses: Error, for serious JVM-level failures, and Exception, for conditions an application may handle; Exception further splits into RuntimeException and checked exceptions. The compiler forces checked exceptions to be caught or declared, while unchecked exceptions are not enforced. The language constructs are try, catch, finally, throw, and, since Java 7, try-with-resources.

## Why interviewers ask this

The interviewer is testing whether you know the exception hierarchy, the difference between checked and unchecked exceptions, how exceptions propagate, and the rules for overriding methods that declare throws. They also want to see that you handle exceptions without swallowing them or losing the root cause, and that you know when to catch, wrap, or let an exception propagate.

## The core idea

The central distinction is checked versus unchecked. Checked exceptions represent expected, often external conditions—like I/O or database failures—that the compiler forces callers to acknowledge. Unchecked exceptions (RuntimeException and Error) represent programming bugs or serious system failures, so the compiler doesn't force handling. When an exception is thrown, the JVM unwinds the call stack until a matching catch block handles it or the thread terminates; finally blocks and try-with-resources run cleanup during unwinding. Strong exception handling catches only what it can actually handle, preserves the original exception as the cause when wrapping, and avoids broad catch blocks that hide errors.

## Key points

- java.lang.Throwable is the root of the exception hierarchy, with two branches: Error for JVM-level failures and Exception for application-level conditions.
- Checked exceptions—Exception subclasses excluding RuntimeException—must be caught or declared in the method signature; RuntimeException and Error are unchecked.
- When an exception is thrown, the JVM propagates it up the call stack until a matching catch is found or the thread terminates.
- An overriding method may throw the same or a more specific checked exception as the overridden method, but never a broader or new checked exception.
- Since Java 7, try-with-resources auto-closes AutoCloseable resources in reverse declaration order and adds any close failure as a suppressed exception to the primary one.

## Your 60-second answer

In Java, every exception and error inherits from java.lang.Throwable. Throwable has two main branches: Error for serious JVM-level failures such as OutOfMemoryError that you normally don't try to catch, and Exception for conditions your code might be able to handle. Exception splits into RuntimeException and checked exceptions. RuntimeExceptions like NullPointerException are unchecked, meaning they usually indicate programming bugs and don't need to be declared. Checked exceptions like IOException must either be caught or declared in the method signature. When an exception is thrown, the JVM unwinds the call stack looking for a matching catch block; if none is found, the thread terminates. The trade-off is that checked exceptions force callers to handle expected failures, but they can create boilerplate and tight coupling, which is why some newer Java APIs prefer unchecked exceptions.

## If they dig deeper

**What is the difference between checked and unchecked exceptions?**

Checked exceptions are all Exception subclasses except RuntimeException; the compiler forces you to either catch them or declare them with throws. Unchecked exceptions are RuntimeException and its subclasses plus Error, and they require no compile-time handling because they usually indicate programming bugs or JVM failures.

**How does exception propagation work?**

When an exception is thrown, the JVM searches the current method for a matching catch block. If none is found, it unwinds to the caller and repeats the search, continuing up the stack. If no catch is found, the thread terminates and the uncaught exception handler prints the stack trace.

**What are the rules when overriding a method that declares a checked exception?**

The overriding method may throw the same exception, a subclass of it, or no checked exception at all. It cannot throw a broader checked exception or a new checked exception because callers of the supertype only expect to handle the exceptions declared by the supertype method. Unchecked exceptions are not constrained.

**When should you catch an exception versus letting it propagate?**

Catch an exception only when you can handle it, add useful context, or translate it at a module boundary. If you cannot recover, let it propagate or wrap it in a more appropriate exception, preserving the original as the cause. Catching and ignoring a failure is usually worse than crashing.

**How does try-with-resources differ from a finally block when closing resources?**

Since Java 7, try-with-resources automatically closes resources that implement AutoCloseable in reverse order of declaration, even if the try block throws. If both the try body and a close operation throw, the close exception is attached as a suppressed exception to the primary exception, so the original failure is not lost. A manual finally block can easily hide the original exception if close also throws.

## Worked example

Consider a loadConfig() method that calls Files.readString(path) and then Integer.parseInt on a line. Files.readString declares IOException, so loadConfig must either catch it or declare throws IOException. Integer.parseInt throws NumberFormatException, which is unchecked, so no declaration is needed. If the file contains a non-numeric line, parseInt throws NumberFormatException; if loadConfig doesn't catch it and its caller doesn't either, the JVM prints a stack trace showing main -> loadConfig -> parseInt and terminates the thread. If loadConfig instead catches IOException because it cannot recover, it might wrap it in a custom ConfigException with the original IOException as the cause and throw that. The caller can then catch ConfigException and call getCause() to inspect the underlying I/O problem.

## Common traps

- Catching Exception or Throwable broadly can hide programming bugs and serious Errors that should propagate.
- An empty catch block swallows the exception and destroys the evidence of what failed; at minimum log it or rethrow a contextual exception.
- Wrapping an exception without passing the original as the cause loses the root cause, making the stack trace less useful.
- Declaring a broader checked exception in an overriding method does not compile because callers of the supertype cannot see the new exception.

</details>

---

## Error cause (`error-cause-match` · match)

### 45. CDN · Hard

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-cdn` then `match: Match each CDN failure scenario with its most likely root ca`</sub>

**Question**

Match each CDN failure scenario with its most likely root cause.

**Options**

**Left**: A user receives another user's personalized page, A popular object expires and the origin is overwhelmed, Users see an old image after the origin file is replaced, A client is routed to a distant edge
**Right**: The cached copy has not expired and no purge was issued, DNS resolution returned an IP far from the client's actual location, A personalized response was cached at the edge, Many edges simultaneously fetch the same object

**Answer (the reader is graded on)**

- 0 ↔ 2 · 1 ↔ 3 · 2 ↔ 0 · 3 ↔ 1

**Why (right answer, wrong reason is wrong)**

→ **A. Because the CDN's DNS uses the client's resolver location, which may be far from the client.**
  B. Because the CDN's anycast routing always sends the client to the nearest edge.
  C. Because the client's browser cache stored an old DNS record.
  D. Because the CDN's DNS does not support GeoIP routing.

**Reference answer**

A user receives another user's personalized page because a personalized response was cached at the edge. A popular object expires and the origin is overwhelmed because many edges simultaneously fetch the same object. Users see an old image after the origin file is replaced because the cached copy has not expired and no purge was issued. A client is routed to a distant edge because DNS resolution returned an IP far from the client's actual location.

**Graded on**

- Caching personalized content can leak user data.
- A cache stampede occurs when many edges miss the same object at once.
- Stale content persists until TTL expiry or explicit purge.
- DNS-based routing can misdirect clients if resolver location is used.

<details><summary>The lesson this came from</summary>

A CDN is a globally distributed system of edge servers that cache content and deliver it from locations close to end users, rather than forcing every request to travel to the origin server. Clients are directed to a nearby edge through DNS-based routing or anycast; an edge serves a cached response if it is fresh, and otherwise fetches, stores, and then serves the object from the origin. CDNs are most effective for static assets such as images, CSS, JavaScript, video, and downloads, but many also accelerate dynamic traffic by terminating TLS and optimizing the path to the origin. Cache behavior is governed by HTTP headers like Cache-Control, and entries can be removed by purge or bypassed with versioned URLs.

## Why interviewers ask this

In system design interviews, CDN questions test whether a candidate knows when to place a cache between users and origin and how to keep the cached data correct. Interviewers look for the ability to separate static from dynamic content, choose TTL and invalidation strategy, and explain the flow of a cache miss. They also probe the operational tradeoffs: stale content, cache hit ratio, origin offload, and DDoS protection.

## The core idea

At its core, a CDN is a distributed cache. The origin server remains the source of truth, while edge servers store copies of immutable or slowly changing objects and absorb most read traffic. A request is routed to the closest edge by the CDN's DNS or anycast network; on a miss, the edge pulls the object from the origin once and then serves subsequent requests locally. This shortens the network path for users and reduces the number of requests hitting the origin, which also makes the origin harder to overwhelm with a DDoS attack. The main design decisions are what to cache, how long to keep it, and how to invalidate it.

## Key points

- A CDN is a network of edge servers that serve cached content from locations geographically close to users, reducing latency and origin load.
- Requests are directed to a nearby edge via DNS resolution or anycast; a cache miss fetches from the origin and stores the response for later hits.
- Static assets like images, CSS, JavaScript, and video are the best CDN candidates because they are identical for many users and change rarely.
- Caching freshness is controlled by HTTP cache headers such as Cache-Control and Expires, and invalidation is done by purging or by changing the URL when content changes.
- CDNs also improve availability and absorb DDoS attacks by spreading traffic across many edge locations and only forwarding cache misses to the origin.

## Your 60-second answer

A CDN is a geographically distributed network of edge servers that cache content and serve it close to users. When a client requests an asset, the CDN's DNS resolution directs the client to the nearest edge server rather than the origin. If the edge has a fresh cached copy, it sends that copy directly, which eliminates the delay of crossing a long distance and removes load from your origin. If it is a miss, the edge pulls the object from the origin once, stores it according to its cache headers, and serves the user; later requests near that edge hit the cache. The core tradeoff is freshness versus speed: cached content can be stale until the TTL expires or you actively purge it. That is why static files like images, CSS, and JavaScript are ideal for CDN caching, while personalized or rapidly changing responses usually require a different strategy.

## If they dig deeper

**What kinds of content should you put on a CDN?**

Static, cacheable assets such as images, CSS, JavaScript, fonts, videos, and downloadable files, because they are the same for many users and do not change often. Personalized or frequently changing content should either bypass full caching or use very short TTLs and fragment-level caching, otherwise you risk serving another user's data.

**How does a client actually get routed to the nearest CDN edge?**

Usually the hostname is delegated to the CDN, and the CDN's authoritative DNS returns the IP address of an edge close to the client's resolver, using GeoIP or similar routing. With anycast, the CDN announces the same IP from many edges, and BGP routes packets to the network-closest point; many CDNs combine DNS steering and anycast.

**What happens when a CDN has a cache miss, and how do you invalidate a stale object?**

On a miss, the edge contacts the origin, fetches the full response, stores it locally for the duration specified by Cache-Control or other cache headers, and returns it to the client. Invalidation can be done by sending a purge request to the CDN for the URL, or more reliably by versioning the filename or query string so changed content is treated as a new cache key.

**CDNs are great for static files, but how do they help with dynamic content?**

They usually do not cache the full dynamic response unless it is explicitly public and cacheable. Instead, they terminate TLS at the edge to reduce handshake latency, keep warm connections to the origin, and route over optimized backbone links; some CDNs also run edge code to assemble personalized fragments or serve API responses from edge key-value stores.

**If you had to design a CDN from scratch, what are the main components you would need?**

You need edge points of presence with cache servers, a request routing layer based on DNS or anycast, and a way for edges to fetch from origin. The harder parts are cache consistency and purge propagation, protecting the origin from a stampede when a popular object expires, TLS certificate management for many customer domains, and DDoS scrubbing at the edge.

## Worked example

A user in London requests https://cdn.example.com/hero.jpg. The hostname resolves through the CDN's DNS to an edge server in London because the CDN's DNS returns the address of the nearest edge. The edge checks its cache; this is the first request for that object, so it is a miss. The edge opens a connection to the origin, fetches the image, stores it with the TTL from the Cache-Control header, and returns the bytes to the user. A second London user requesting the same URL soon after is served directly from the London edge with no origin contact. If the marketing team later publishes a new hero image at the same URL, users may continue receiving the cached old image until its TTL expires or the CDN receives a purge. The safe fix is to version the URL, such as /hero-v2.jpg, so the new asset has a distinct cache key and is fetched immediately.

## Common traps

- Assuming a CDN replaces the origin or is a separate copy of the whole database, without realising the origin remains the source of truth for misses and writes.
- Caching personalized or user-specific pages because they seem static, which can leak one user's data to another.
- Changing a file on the origin and expecting users to see the new version immediately while a long Cache-Control or CDN TTL is still active.
- Forgetting that DNS changes take time to propagate and that moving a domain onto or off a CDN can leave clients talking to old servers if CNAME and TTL changes are not handled carefully.

</details>

---

### 46. API Gateway · Hard

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-api-gateway` then `match: Match each API gateway failure scenario with its most likely`</sub>

**Question**

Match each API gateway failure scenario with its most likely root cause.

**Options**

**Left**: A single slow downstream service causes all API requests to time out, A client exceeds the global rate limit by sending requests to different gateway instances, Every feature change requires a gateway deployment, The entire API becomes unavailable when the rate limiter service goes down
**Right**: No fail-open/fail-closed policy for critical dependencies, Business logic embedded in the gateway, Missing circuit breakers and timeouts, Per-instance in-memory rate limit counters

**Answer (the reader is graded on)**

- 0 ↔ 2 · 1 ↔ 3 · 2 ↔ 1 · 3 ↔ 0

**Why (right answer, wrong reason is wrong)**

→ **A. Because a circuit breaker stops sending requests to a failing service and returns a fallback response, preventing thread exhaustion.**
  B. Because a circuit breaker increases the number of retries to the failing service, ensuring requests eventually succeed.
  C. Because a circuit breaker caches responses from the failing service, reducing load on the gateway.
  D. Because a circuit breaker redirects requests to a different service instance, avoiding the slow one.

**Reference answer**

The correct pairings are: (1) A single slow downstream service causes all API requests to time out → missing circuit breakers and timeouts; (2) A client exceeds the global rate limit by sending requests to different gateway instances → per-instance in-memory rate limit counters; (3) Every feature change requires a gateway deployment → business logic embedded in the gateway; (4) The entire API becomes unavailable when the rate limiter service goes down → no fail-open/fail-closed policy for critical dependencies.

**Graded on**

- Without circuit breakers, a slow service can exhaust gateway threads and block all traffic.
- Per-instance rate limit counters allow clients to bypass global limits by spreading requests across instances.
- Embedding business logic in the gateway forces frequent gateway deployments.
- A gateway that fails closed on a critical dependency like the rate limiter can take down the whole API.

<details><summary>The lesson this came from</summary>

An API gateway is a reverse proxy that accepts all client API calls, applies cross-cutting policies, and forwards each request to the appropriate backend service. In a microservices architecture it hides internal service boundaries behind one client-facing endpoint, handling authentication, authorization, rate limiting, load balancing, caching, request/response transformation, and observability. The gateway itself should contain no business logic; it manages traffic and policy at the edge.

## Why interviewers ask this

At Amazon, Atlassian, Uber, and Patreon, rate-limiter questions probe the same component because gateways are the natural enforcement point. The interviewer is testing whether you can design a single entry point that remains correct under concurrency, scales horizontally, and fails without taking the whole system down. They also look for separation of cross-cutting concerns from business logic.

## The core idea

The gateway is the edge policy engine. It terminates client TLS, authenticates the caller, checks quotas, and then routes the request according to path, method, and headers. It may also compose responses from multiple services or cache them so backend load drops. Because all traffic passes through it, it becomes both the best place to enforce organization-wide rules and the most dangerous single point of failure. A strong design keeps it stateless, horizontally scaled, and equipped with timeouts, retries, and circuit breakers. The routing table or service discovery layer tells it where each request should go without embedding service addresses in clients.

## Key points

- An API gateway terminates client TLS, authenticates requests, authorizes per route, and proxies to backend services, so individual services do not repeat these checks.
- Rate limiting at the gateway can use token bucket or sliding window algorithms; in a distributed deployment the counters must live in a shared store such as Redis rather than per-instance memory.
- API composition lets the gateway call multiple services and merge responses to reduce client round trips, but it adds gateway latency and complexity.
- The gateway must be stateless and horizontally scalable behind a load balancer, with health checks, timeouts, retries, and circuit breakers to avoid cascading failures.
- Common gateway implementations include AWS API Gateway, Kong, and NGINX/OpenResty, though features and configuration models vary by product.

## Your 60-second answer

An API gateway is a single entry point that sits between clients and backend services. It receives every API request, terminates TLS, authenticates the caller, enforces rate limits, and routes the request to the correct service. It also handles cross-cutting concerns like caching, request and response transformation, and monitoring, so downstream services don't duplicate that work. The reason you add one is that microservices expose many fine-grained endpoints; a gateway composes them into one client-friendly API and applies policies at the edge. The main trade-off is that it becomes a critical path: if it fails or is misconfigured, all traffic stops. So you run multiple stateless instances, set timeouts and circuit breakers, and avoid putting business logic in the gateway.

## If they dig deeper

**What are the core responsibilities of an API gateway?**

Routing requests to the correct backend, authentication and authorization, rate limiting, load balancing, caching, request/response transformation, and observability. It can also do API composition, calling multiple services and merging responses. It should not contain business logic.

**How would you implement authentication and authorization at the gateway?**

Validate the caller's credential, usually a JWT or OAuth2 token, at the edge by checking signature, expiry, issuer, and audience. On failure return 401; after authentication check scopes or roles against the route and return 403 if insufficient. Then forward the request with trusted identity headers to downstream services.

**How do you implement rate limiting at the gateway?**

Identify the client by API key, user ID, or IP address. For a single gateway instance, keep a token bucket or sliding window counter in memory; for multiple instances, store counters in Redis with atomic operations. When the limit is exceeded, return HTTP 429 with Retry-After and rate limit headers.

**How do you scale rate limiting across many gateway instances?**

Share the counter state in a central store like Redis and use atomic Lua scripts or sorted sets for sliding windows. Fixed-window counters are simpler but can allow bursts at window boundaries; sliding window log gives accuracy at higher memory cost. If per-instance counters are used, clients can exceed the global limit by hitting different instances, so a shared store is usually required.

**How do you make the gateway fault tolerant and prevent it from becoming a bottleneck?**

Run multiple stateless gateway instances behind a load balancer, set aggressive timeouts, use circuit breakers to stop calling unhealthy services, and retry only idempotent requests. Cache safe responses, monitor CPU and connection saturation, and decide whether to fail open or fail closed when the rate limiter or auth service is unavailable. Keep the gateway free of business logic so changes are rare and deployments are low-risk.

## Worked example

A mobile client sends POST /orders to the gateway. The gateway terminates TLS, validates the JWT signature and expiry, and reads the user ID. It checks a token bucket in Redis for key rate:user:123. The bucket has capacity 100 and refills 10 tokens per second; at this moment 4 tokens remain because the user has consumed 96 requests in the current minute. The gateway allows the request, decrements the bucket to 3, and forwards it to the order service with an X-User-Id header. The order service returns 201, and the gateway strips internal fields before returning JSON. After three more rapid requests the bucket reaches 0, so the next request receives HTTP 429 with Retry-After: 30 and X-RateLimit-Remaining: 0.

## Common traps

- Putting business logic in the gateway, which turns it into a distributed monolith and forces a gateway deployment for every feature change.
- Using per-instance in-memory counters for rate limiting in a multi-instance deployment, allowing a client to exceed the global limit by spreading requests across instances.
- Forgetting timeouts and circuit breakers, so a slow downstream service consumes all gateway threads and makes every API unavailable.
- Assuming the gateway will never fail and not planning redundancy or a fail-open/fail-closed policy, which creates a single point of failure.

</details>

---

## Pattern signal (`pattern-signal` · match)

### 47. Graphs · Hard

*dsa · gate confidence 0.9*

<sub>to object to this card: `## graphs` then `match: Match each graph problem to the pattern that best solves it.`</sub>

**Question**

Match each graph problem to the pattern that best solves it. Assume standard constraints: unweighted edges, no negative weights, and the problem is solved optimally.

**Options**

**Left**: Number of Islands, Course Schedule, Pacific Atlantic Water Flow, Graph Valid Tree, Number of Connected Components in an Undirected Graph, Clone Graph
**Right**: Union-Find / DSU, Kahn's Topological Sort, Boundary/Reverse Traversal, DFS/BFS Component Traversal, Multi-source BFS, Level-by-Level BFS

**Answer (the reader is graded on)**

- 0 ↔ 3 · 1 ↔ 1 · 2 ↔ 2 · 3 ↔ 0 · 4 ↔ 3 · 5 ↔ 3

**Why (right answer, wrong reason is wrong)**

  A. Because it processes nodes in order of increasing indegree, which is the only way to detect cycles in a directed graph.
→ **B. Because it repeatedly removes nodes with zero indegree; if a cycle exists, some nodes never reach zero indegree, so fewer than all nodes are processed.**
  C. Because it uses a min-heap to always expand the node with the smallest indegree, guaranteeing all nodes are visited.
  D. Because it performs a DFS from every node and checks for back edges, which is more efficient than BFS for cycle detection.

**Reference answer**

Number of Islands uses DFS/BFS component traversal to count connected land components. Course Schedule uses Kahn's topological sort to detect cycles in a directed prerequisite graph. Pacific Atlantic Water Flow uses boundary/reverse traversal from ocean cells to find cells reachable from both oceans. Graph Valid Tree uses Union-Find/DSU to detect cycles and check connectivity. Number of Connected Components uses DFS/BFS component traversal to count components. Clone Graph uses DFS/BFS with a visited map to deep-copy nodes and edges.

**Graded on**

- Component counting problems map to DFS/BFS traversal with a visited set.
- Cycle detection in directed graphs maps to Kahn's topological sort.
- Problems asking for cells reachable from boundaries map to reverse traversal from those boundaries.
- Tree validation maps to Union-Find/DSU for cycle detection and connectivity.

<details><summary>The lesson this came from</summary>

A graph is a collection of vertices connected by edges, used to model arbitrary relationships such as prerequisites, network connections, or grid adjacency. Code represents graphs with adjacency lists or adjacency matrices; adjacency lists are the default for sparse graphs. Traversal uses DFS or BFS with an explicit visited set because graphs may contain cycles. Common graph tasks reduce to counting connected components, detecting cycles, finding unweighted shortest paths, or ordering nodes topologically.

## Why interviewers ask this

Interviewers use graph problems to test whether you can recognize a hidden graph model, choose DFS versus BFS, and handle cycles and visited state. Graph problems like Number of Islands, Course Schedule, Clone Graph, and Word Ladder appear frequently across companies including TikTok, Snowflake, Meta, LinkedIn, and Snap. The signal is not just writing a traversal but translating a domain constraint into graph structure without infinite loops.

## The core idea

Graphs generalize trees; the critical change is explicit visited tracking. Once a problem is modeled as nodes and edges, most interview questions fall into four patterns: connected components, cycle detection, unweighted shortest path, and topological sort. Grids are implicit graphs, where each cell connects to up to four neighbors. Weighted graphs require Dijkstra's algorithm with a min-heap, not plain BFS. The difficult part is usually recognizing which pattern applies, not writing the traversal itself.

## Key points

- Adjacency-list storage costs O(V + E) space, while an adjacency matrix costs O(V^2) space and gives O(1) edge existence checks.
- DFS and BFS both run in O(V + E) time on an adjacency-list graph when each node and edge is processed once.
- BFS gives shortest paths in unweighted graphs; Dijkstra's algorithm handles non-negative weighted graphs using a min-heap.
- A directed graph has a valid topological sort exactly when it is a directed acyclic graph; Kahn's algorithm processes nodes whose indegree becomes zero.
- In a 2D grid, a cell is a node and its four orthogonal neighbors are edges, so grid dimensions define an implicit graph of size rows × columns.

## Your 60-second answer

Graphs are a way to model objects as vertices and relationships as edges. In code I use adjacency lists most of the time because they take O(V + E) space, and I traverse with DFS or BFS while keeping a visited set to avoid revisiting nodes through cycles. For unweighted shortest paths, BFS is the right tool because it expands in distance order. For prerequisites and ordering, I detect cycles and build a topological sort with Kahn's algorithm on indegrees. In a grid, each cell is a node and its four neighbors are edges. The trade-off is that an adjacency matrix gives constant-time edge checks but costs O(V^2) memory, so I only use it for dense graphs or when I need many edge lookups.

## If they dig deeper

**How do you represent a graph in code, and when would you choose an adjacency matrix over an adjacency list?**

An adjacency list stores each node's neighbors in a list or map of lists, using O(V + E) space. An adjacency matrix uses a V×V boolean or weight array, giving O(1) edge existence checks but O(V^2) space, so it is only preferred for dense graphs or frequent edge lookups.

**How do you count connected components in an undirected graph?**

Iterate over all nodes. When a node is unvisited, increment the component count and run DFS or BFS from that node, marking reachable nodes as visited. The traversal explores one full component, so the total work is O(V + E).

**How do you detect a cycle in an undirected graph versus a directed graph?**

For an undirected graph, DFS with a parent parameter detects a cycle if a neighbor is already visited and is not the parent. For a directed graph, use DFS with three states or a recursion stack, or run Kahn's algorithm and check whether all nodes were processed; if some remain, a cycle exists.

**When is BFS not sufficient for shortest paths, and what replaces it?**

BFS only gives shortest paths when all edges have weight one or no weights. With weighted edges, Dijkstra's algorithm uses a min-heap to expand nodes in increasing distance order and works for non-negative weights; negative weights require Bellman-Ford.

**How would you solve Pacific Atlantic Water Flow, where water can flow downhill to adjacent cells of equal or lower height?**

Run a multi-source BFS or DFS from all cells touching the Pacific and separately from all cells touching the Atlantic, but traverse in reverse: move only to neighbors whose height is greater than or equal to the current cell. Mark reachable cells from each ocean, then return the intersection of the two reachable sets.

## Worked example

For Course Schedule with numCourses = 2 and prerequisites = [[1,0],[0,1]], interpret each pair [a,b] as a directed edge b -> a. The graph has edge 0 -> 1 and edge 1 -> 0. Compute indegrees: node 0 has indegree 1, node 1 has indegree 1. Kahn's algorithm starts with a queue containing all nodes with indegree 0, but no such node exists, so the queue is empty. The processed-node count remains 0, which is less than numCourses = 2, so the algorithm reports a cycle and the method returns false.

## Common traps

- Forgetting the visited/seen set in a cyclic graph, leading to infinite recursion in DFS or repeated enqueueing in BFS.
- Using plain BFS for shortest paths in a weighted graph; it is only guaranteed for unweighted edges.
- Treating the edge back to the DFS parent as a cycle in undirected cycle detection instead of skipping the parent.
- Assuming one DFS or BFS from a single source covers the whole graph; disconnected graphs need a loop over all unvisited nodes.

</details>

---

## Operation complexity (`operation-complexity` · match)

### 48. OOP Concepts · Hard

*java · gate confidence 0.8*

<sub>to object to this card: `## java-oop-concepts` then `match: Match each Java OOP concept or feature with its runtime or c`</sub>

**Question**

Match each Java OOP concept or feature with its runtime or compile-time behavior. Assume standard Java semantics and a typical JVM implementation.

**Options**

**Left**: Encapsulation, Inheritance, Polymorphism, Abstraction, Primitive types, Static members
**Right**: Resolved at compile time based on argument types, Belong to the class, not instances, Declares contracts via abstract classes and interfaces, Reuses superclass members through the class hierarchy, Not objects and bypass object dispatch, Dispatches overridden methods based on runtime class

**Answer (the reader is graded on)**

- 0 ↔ 5 · 1 ↔ 3 · 2 ↔ 4 · 3 ↔ 2 · 4 ↔ 1 · 5 ↔ 0

**Why (right answer, wrong reason is wrong)**

→ **A. Because the JVM looks up the method in the object's runtime class method table, not the reference's declared type.**
  B. Because the compiler resolves the method based on the declared type of the reference.
  C. Because all methods are resolved at compile time to improve performance.
  D. Because the runtime class is always the same as the declared type.

**Reference answer**

Encapsulation is enforced by access modifiers at compile time and runtime; inheritance reuses superclass members through the class hierarchy; polymorphism dispatches overridden instance methods based on the object's runtime class; abstraction declares contracts via abstract classes and interfaces; primitives are not objects and bypass object dispatch; static members belong to the class, not instances.

**Graded on**

- Encapsulation uses private fields and public methods to protect invariants.
- Polymorphism resolves overridden methods using the runtime class's method table.
- Java supports single inheritance but multiple interface implementation.
- Primitives and static members exist outside the object model.

<details><summary>The lesson this came from</summary>

Object-oriented programming organizes code into classes that bundle state (fields) with behavior (methods). In Java, classes act as blueprints, instance fields hold per-object state, and methods operate on that state. The four core principles are encapsulation (restricting access to internal state), inheritance (subclassing a parent type), polymorphism (dispatching calls based on the actual object's runtime type), and abstraction (exposing only essential behavior through abstract classes and interfaces).

## Why interviewers ask this

Interviewers use OOP questions to test whether you can design cohesive classes, protect invariants with access control, and explain runtime dispatch versus compile-time resolution. They also probe Java-specific mechanics—single inheritance, interfaces, Object methods, and where Java is not purely object-oriented—so a candidate who only recites definitions fails. Strong answers connect each principle to a concrete Java feature or failure mode.

## The core idea

OOP binds data and the operations on it into one unit, so an object's state changes only through its methods. Encapsulation is enforced in Java with access modifiers: private fields hide representation, protected exposes to subclasses and the package, and public methods provide behavior. Inheritance allows a subclass to reuse a parent's fields and methods; Java permits exactly one superclass but many interfaces. Polymorphism means a variable of type Shape can hold a Circle, and a call like shape.area() executes Circle's override using the runtime class's method table. Abstraction lets abstract classes and interfaces declare what an object does without committing to how. Java is not purely OOP because primitives and static members exist outside objects.

## Key points

- In Java, private fields plus public methods are the standard encapsulation mechanism, and protected means accessible within the package and subclasses.
- Java implements polymorphism through dynamic dispatch: overridden instance methods are resolved from the object's runtime class, not the reference's declared type.
- A Java class can extend only one superclass but can implement any number of interfaces; default methods can cause conflicts that must be explicitly resolved.
- Every Java class implicitly extends Object, so all objects inherit equals, hashCode, toString, getClass, and thread coordination methods like wait and notify.
- Java is not purely object-oriented because primitives (int, boolean, double) and static members can be used without any object instance.

## Your 60-second answer

Object-oriented programming in Java means designing programs as objects that combine state (fields) and behavior (methods). The four core ideas are encapsulation, inheritance, polymorphism, and abstraction. Encapsulation hides internal state behind private fields and exposes behavior through public methods, which protects invariants. Inheritance lets a class extend one superclass and inherit its fields and methods, while interfaces allow multiple type contracts. Polymorphism means a superclass or interface reference can point to a subclass object, and the JVM dispatches the overridden method based on the actual object's runtime type, not the reference type. Abstraction uses abstract classes and interfaces to define what an object does without specifying how. The trade-off is that inheritance creates tight coupling, so composition is often preferred for flexibility; Java is considered not purely OOP because primitives and statics live outside the object model.

## If they dig deeper

**When can an object reference be cast to a Java interface reference?**

An object reference can be cast to an interface type when the object's actual runtime class implements that interface. The JVM checks the cast at runtime and throws ClassCastException if the object does not implement it; upcasting to an interface is implicit, while casting back to a concrete class requires an explicit cast. This is the basis of programming to interfaces.

**What is the difference between an abstract class and an interface in Java?**

An abstract class can have instance fields, constructors, and concrete methods, so it can carry shared state and enforce a base implementation. An interface primarily declares a contract, though since Java 8 it can have default and static methods, and since Java 9 private methods. A class extends one abstract class but can implement many interfaces, so use an interface for a capability and an abstract class for shared implementation.

**Why is Java not considered a purely object-oriented language?**

Java has primitive types like int, boolean, and double that are not objects, and static variables and methods can be used without any instance. Operations on primitives and static calls are not dispatched through objects. Java intentionally kept primitives for performance and uses wrapper classes only when objects are needed.

**What methods does java.lang.Object define, and why must equals and hashCode be overridden together?**

Object defines getClass, hashCode, equals, toString, clone, and wait/notify/notifyAll; finalize was deprecated in Java 9. The contract requires equal objects to have equal hash codes, so if you override equals to compare fields, you must override hashCode consistently. Otherwise HashMap and HashSet lookups fail for equal objects that hash differently.

**How can you create an object without the new operator, and when is that appropriate?**

You can use reflection with Class.forName(...).getDeclaredConstructor().newInstance(), call clone() on a class that implements Cloneable, deserialize via ObjectInputStream, or load a class and instantiate it with a class loader. Reflection is slower and less type-safe, clone makes shallow copies unless overridden, and deserialization can bypass constructors and leave invariants uninitialized. Prefer new unless you need runtime plugin loading, copying, or persistence.

## Worked example

Consider an abstract class Shape with an abstract method area(). A Circle stores a radius and overrides area to return Math.PI * radius * radius; a Square stores a side and returns side * side. A method printArea(Shape s) prints s.area(). Calling printArea(new Circle(2)) prints 12.57 because the compiler only knows s is Shape, but at runtime the JVM looks up area in Circle's method table. Calling printArea(new Square(3)) prints 9.0 through the same call site. Adding a Triangle later requires no changes to printArea, which shows polymorphism making code open for extension without modifying existing behavior.

## Common traps

- Confusing overloading with overriding: overload resolution happens at compile time based on argument types, while overriding dispatches at runtime based on the object's class.
- Claiming Java is purely object-oriented when primitives and static members exist outside instances.
- Overriding equals without hashCode, which breaks HashMap and HashSet because equal objects must hash equally.
- Thinking Java supports multiple inheritance because it has interfaces; a class still extends only one superclass, and default method conflicts must be resolved explicitly.

</details>

---

### 49. ConcurrentHashMap · Hard

*java · gate confidence 0.8*

<sub>to object to this card: `## java-concurrenthashmap` then `match: Match each ConcurrentHashMap operation with its synchronizat`</sub>

**Question**

Match each ConcurrentHashMap operation with its synchronization behavior in Java 8. Assume standard implementation and no external synchronization.

**Options**

**Left**: get, put, computeIfAbsent, size
**Right**: Lock-free; reads volatile references, Locks only the target hash bin, Locks the target bin and runs the mapping function atomically, Sums counter cells without locking all bins; weakly consistent

**Answer (the reader is graded on)**

- 0 ↔ 0 · 1 ↔ 1 · 2 ↔ 2 · 3 ↔ 3

**Why (right answer, wrong reason is wrong)**

  A. Because get must acquire a read lock to ensure visibility of concurrent writes.
→ **B. Because volatile reads of the table reference and node fields guarantee visibility without locking.**
  C. Because get uses a global read-write lock that allows multiple readers but excludes writers.
  D. Because get iterates over all bins and locks each one briefly to collect a consistent snapshot.

**Reference answer**

get is lock-free and uses volatile reads. put locks only the target hash bin. computeIfAbsent locks the target bin and performs the mapping function atomically under that lock. size sums base count and counter cells without locking all bins, so it is weakly consistent.

**Graded on**

- get performs volatile reads without acquiring any lock.
- put uses CAS for empty bins and synchronized on the first node for non-empty bins.
- computeIfAbsent holds the bin lock while executing the mapping function.
- size does not lock all bins and may not reflect a single instant.

<details><summary>The lesson this came from</summary>

ConcurrentHashMap is a thread-safe implementation of the Map interface in java.util.concurrent, introduced in Java 5. It allows concurrent reads and updates by restricting synchronization to individual hash bins or segments instead of locking the entire map. Iterators are weakly consistent and do not throw ConcurrentModificationException. Null keys and values are rejected with a NullPointerException.

## Why interviewers ask this

Interviewers ask about ConcurrentHashMap to see whether the candidate understands Java concurrency beyond the synchronized keyword. They want to test knowledge of how real-world concurrent data structures reduce contention, the difference between thread safety and scalability, and the guarantees around iteration and compound operations.

## The core idea

The core idea is to avoid a single map-wide lock. In Java 7 the map was split into segments, each guarded by its own ReentrantLock, so writes to different segments could proceed in parallel. In Java 8 the segment design was replaced by lock-free reads and per-bin synchronization using CAS and synchronized blocks on the first node of a bin. Many reads, including get, perform volatile reads without acquiring a lock. Compound operations such as computeIfAbsent and merge are atomic under the per-key lock, giving both safety and scalability.

## Key points

- ConcurrentHashMap rejects null keys and values, throwing NullPointerException immediately.
- Since Java 8, writes lock only the target hash bin; Java 7 used lock striping over a fixed set of segments.
- get and many read operations are lock-free and rely on volatile reads of table references and node fields.
- Iterators are weakly consistent: they traverse some state of the map and never throw ConcurrentModificationException.
- Java 8 added atomic compound operations such as compute, computeIfAbsent, merge, and forEach with parallelism thresholds.

## Your 60-second answer

ConcurrentHashMap is Java's thread-safe map in java.util.concurrent. It gives you concurrent reads and writes without synchronizing the whole map. In Java 8, reads like get are lock-free because internal table references and node fields are volatile, and writes lock only the hash bin being modified, using CAS for insertions. This makes it much more scalable than Hashtable, which synchronizes every method on one lock. Compound operations like computeIfAbsent and merge are atomic under the per-key lock. It does not allow null keys or values, and iterators are weakly consistent, so they won't throw ConcurrentModificationException but may not reflect every concurrent change. The trade-off is that operations such as size or clear can be less globally consistent than under a single global lock, though they are safe.

## If they dig deeper

**How does ConcurrentHashMap differ from Hashtable?**

Hashtable synchronizes every public method on a single lock, which serializes all operations. ConcurrentHashMap allows concurrent reads and writes to different bins; in Java 8, reads are lock-free and writes lock only the bin being modified. Hashtable also rejects null keys and values, but ConcurrentHashMap achieves higher throughput under contention.

**What changed internally between Java 7 and Java 8?**

Java 7 used a fixed number of segments, each with its own ReentrantLock, and the concurrency level set the segment count. Java 8 removed segments and instead uses synchronized on the first node of a hash bin plus CAS for empty-bin insertion, with tree bins for long chains. The constructor's concurrencyLevel parameter is still accepted but used only for initial sizing.

**What does it mean that iterators are weakly consistent?**

An iterator may or may not reflect modifications made after it was created, but it will never throw ConcurrentModificationException. It traverses elements as they existed at some point and reads volatile references, so values reflect up-to-date memory visibility. size may not be exact during concurrent modification.

**Why does ConcurrentHashMap not allow null keys or values?**

In a concurrent map, get returning null is ambiguous: it could mean the key is absent or the value is null. Allowing null values would make containsKey unreliable and complicate atomic remapping methods like computeIfAbsent and merge. Rejecting null removes that ambiguity.

**How does size() work and is it exact during concurrent updates?**

In Java 8, size() sums a base count and counter cells that are updated with CAS, so it does not lock all bins. The returned value is weakly consistent and may not correspond to any single instant if updates happen concurrently. In Java 7, size could lock all segments to compute an exact value, but that was more expensive.

## Worked example

Thread A calls map.computeIfAbsent("user-1", k -> load(k)); Thread B calls map.put("user-2", user2) at the same time. In Java 8 both can proceed because the keys hash to different bins; computeIfAbsent locks only the bin for user-1 and put locks only the bin for user-2. If two threads call computeIfAbsent for the same key, one blocks on the bin lock while the other computes the value. The second thread then sees the value already present and returns it without recomputing, avoiding duplicate initialization. This demonstrates per-key atomicity and bounded locking.

## Common traps

- Saying ConcurrentHashMap locks the entire map: Java 8 locks per hash bin, Java 7 per segment, never the whole map on every operation.
- Assuming its iterators are fail-fast or throw ConcurrentModificationException like HashMap.
- Assuming size() returns an exact global snapshot during concurrent updates.
- Thinking it allows null keys or values because HashMap does; it throws NullPointerException.

</details>

---

## API guarantee (`api-guarantee` · match)

### 50. CDN · Easy

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-cdn` then `match: Match each CDN concept to its description.`</sub>

**Question**

Match each CDN concept to its description.

**Options**

**Left**: CDN, Edge server, Cache miss, Cache-Control, Static asset, Purge, Versioned URL, Origin server
**Right**: A network of geographically distributed servers that cache content and serve it close to users, A server in a CDN that stores cached copies of content and serves nearby users, A request for content that is not in the edge cache, causing the edge to fetch it from the origin, An HTTP header that specifies how long a cached response may be considered fresh, A file such as an image, CSS, or JavaScript that is identical for many users and changes rarely, An operation that removes a cached object from CDN edge servers before its TTL expires, A URL that includes a version identifier so that changed content is treated as a new cache key, The server that holds the authoritative copy of the content and serves cache misses

**Answer (the reader is graded on)**

- 0 ↔ 0 · 1 ↔ 1 · 2 ↔ 2 · 3 ↔ 3 · 4 ↔ 4 · 5 ↔ 5 · 6 ↔ 6 · 7 ↔ 7

**Reference answer**

A CDN is a distributed cache: edge servers serve cached content close to users, reducing latency and origin load. Requests are routed to a nearby edge via DNS or anycast; a cache miss fetches from the origin and stores the response for later hits. Static assets like images, CSS, and JavaScript are ideal because they are identical for many users and change rarely. Cache freshness is controlled by HTTP headers such as Cache-Control, and invalidation is done by purging or changing the URL when content changes.

**Graded on**

- A CDN is a network of edge servers that serve cached content from locations geographically close to users.
- Requests are directed to a nearby edge via DNS resolution or anycast; a cache miss fetches from the origin and stores the response.
- Static assets like images, CSS, JavaScript, and video are the best CDN candidates because they are identical for many users and change rarely.
- Caching freshness is controlled by HTTP cache headers such as Cache-Control and Expires, and invalidation is done by purging or by changing the URL when content changes.

<details><summary>The lesson this came from</summary>

A CDN is a globally distributed system of edge servers that cache content and deliver it from locations close to end users, rather than forcing every request to travel to the origin server. Clients are directed to a nearby edge through DNS-based routing or anycast; an edge serves a cached response if it is fresh, and otherwise fetches, stores, and then serves the object from the origin. CDNs are most effective for static assets such as images, CSS, JavaScript, video, and downloads, but many also accelerate dynamic traffic by terminating TLS and optimizing the path to the origin. Cache behavior is governed by HTTP headers like Cache-Control, and entries can be removed by purge or bypassed with versioned URLs.

## Why interviewers ask this

In system design interviews, CDN questions test whether a candidate knows when to place a cache between users and origin and how to keep the cached data correct. Interviewers look for the ability to separate static from dynamic content, choose TTL and invalidation strategy, and explain the flow of a cache miss. They also probe the operational tradeoffs: stale content, cache hit ratio, origin offload, and DDoS protection.

## The core idea

At its core, a CDN is a distributed cache. The origin server remains the source of truth, while edge servers store copies of immutable or slowly changing objects and absorb most read traffic. A request is routed to the closest edge by the CDN's DNS or anycast network; on a miss, the edge pulls the object from the origin once and then serves subsequent requests locally. This shortens the network path for users and reduces the number of requests hitting the origin, which also makes the origin harder to overwhelm with a DDoS attack. The main design decisions are what to cache, how long to keep it, and how to invalidate it.

## Key points

- A CDN is a network of edge servers that serve cached content from locations geographically close to users, reducing latency and origin load.
- Requests are directed to a nearby edge via DNS resolution or anycast; a cache miss fetches from the origin and stores the response for later hits.
- Static assets like images, CSS, JavaScript, and video are the best CDN candidates because they are identical for many users and change rarely.
- Caching freshness is controlled by HTTP cache headers such as Cache-Control and Expires, and invalidation is done by purging or by changing the URL when content changes.
- CDNs also improve availability and absorb DDoS attacks by spreading traffic across many edge locations and only forwarding cache misses to the origin.

## Your 60-second answer

A CDN is a geographically distributed network of edge servers that cache content and serve it close to users. When a client requests an asset, the CDN's DNS resolution directs the client to the nearest edge server rather than the origin. If the edge has a fresh cached copy, it sends that copy directly, which eliminates the delay of crossing a long distance and removes load from your origin. If it is a miss, the edge pulls the object from the origin once, stores it according to its cache headers, and serves the user; later requests near that edge hit the cache. The core tradeoff is freshness versus speed: cached content can be stale until the TTL expires or you actively purge it. That is why static files like images, CSS, and JavaScript are ideal for CDN caching, while personalized or rapidly changing responses usually require a different strategy.

## If they dig deeper

**What kinds of content should you put on a CDN?**

Static, cacheable assets such as images, CSS, JavaScript, fonts, videos, and downloadable files, because they are the same for many users and do not change often. Personalized or frequently changing content should either bypass full caching or use very short TTLs and fragment-level caching, otherwise you risk serving another user's data.

**How does a client actually get routed to the nearest CDN edge?**

Usually the hostname is delegated to the CDN, and the CDN's authoritative DNS returns the IP address of an edge close to the client's resolver, using GeoIP or similar routing. With anycast, the CDN announces the same IP from many edges, and BGP routes packets to the network-closest point; many CDNs combine DNS steering and anycast.

**What happens when a CDN has a cache miss, and how do you invalidate a stale object?**

On a miss, the edge contacts the origin, fetches the full response, stores it locally for the duration specified by Cache-Control or other cache headers, and returns it to the client. Invalidation can be done by sending a purge request to the CDN for the URL, or more reliably by versioning the filename or query string so changed content is treated as a new cache key.

**CDNs are great for static files, but how do they help with dynamic content?**

They usually do not cache the full dynamic response unless it is explicitly public and cacheable. Instead, they terminate TLS at the edge to reduce handshake latency, keep warm connections to the origin, and route over optimized backbone links; some CDNs also run edge code to assemble personalized fragments or serve API responses from edge key-value stores.

**If you had to design a CDN from scratch, what are the main components you would need?**

You need edge points of presence with cache servers, a request routing layer based on DNS or anycast, and a way for edges to fetch from origin. The harder parts are cache consistency and purge propagation, protecting the origin from a stampede when a popular object expires, TLS certificate management for many customer domains, and DDoS scrubbing at the edge.

## Worked example

A user in London requests https://cdn.example.com/hero.jpg. The hostname resolves through the CDN's DNS to an edge server in London because the CDN's DNS returns the address of the nearest edge. The edge checks its cache; this is the first request for that object, so it is a miss. The edge opens a connection to the origin, fetches the image, stores it with the TTL from the Cache-Control header, and returns the bytes to the user. A second London user requesting the same URL soon after is served directly from the London edge with no origin contact. If the marketing team later publishes a new hero image at the same URL, users may continue receiving the cached old image until its TTL expires or the CDN receives a purge. The safe fix is to version the URL, such as /hero-v2.jpg, so the new asset has a distinct cache key and is fetched immediately.

## Common traps

- Assuming a CDN replaces the origin or is a separate copy of the whole database, without realising the origin remains the source of truth for misses and writes.
- Caching personalized or user-specific pages because they seem static, which can leak one user's data to another.
- Changing a file on the origin and expecting users to see the new version immediately while a long Cache-Control or CDN TTL is still active.
- Forgetting that DNS changes take time to propagate and that moving a domain onto or off a CDN can leave clients talking to old servers if CNAME and TTL changes are not handled carefully.

</details>

---

### 51. Design a notification system · Easy

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-design-a-notification-system` then `match: Match each notification system component with the delivery g`</sub>

**Question**

Match each notification system component with the delivery guarantee it provides.

**Options**

**Left**: Notification gateway to business service, Durable queue to worker, Channel adapter to provider (FCM/APNs), End-to-end to user (with client deduplication)
**Right**: At-least-once, At-most-once, At-least-once, 202 Accepted (acknowledgment, not delivery)

**Answer (the reader is graded on)**

- 0 ↔ 3 · 1 ↔ 0 · 2 ↔ 2 · 3 ↔ 1

**Reference answer**

The notification gateway returns 202 Accepted to business services, acknowledging receipt without waiting for delivery. The durable queue provides at-least-once delivery to workers, ensuring no message is lost even if a worker crashes. The channel adapter (e.g., FCM/APNs call) provides at-least-once delivery to the provider, but the provider may deliver duplicates. End-to-end delivery to the user is at-most-once from the user's perspective if the client deduplicates, but without deduplication it is at-least-once.

**Graded on**

- The gateway acknowledges receipt with 202, not delivery.
- The durable queue guarantees at-least-once delivery to workers.
- External providers like FCM/APNs are at-least-once, so duplicates are possible.
- Client-side deduplication can make user-visible delivery effectively at-most-once.

<details><summary>The lesson this came from</summary>

A notification system is backend infrastructure that accepts notification requests from business services, validates and formats them, and dispatches messages to users over channels such as in-app real-time connections, mobile push providers, email, or SMS. It typically has a gateway, a distribution layer that applies templates and user preferences, durable queues, and channel-specific workers. For mobile push, the backend calls platform providers like FCM for Android and APNs for iOS using per-device tokens; for in-app delivery it may push over a WebSocket connection. The system also records delivery callbacks for retry and analytics.

## Why interviewers ask this

The interviewer is testing whether you can turn a vague 'notify the user' requirement into components with clear responsibilities, handle external provider failures, and scale an asynchronous pipeline. They also probe whether you understand that mobile push has different delivery semantics from in-app streaming, and that external providers impose at-least-once behavior. Strong candidates ask about channels, volume, and latency before drawing a diagram.

## The core idea

Treat sending a notification as an asynchronous pipeline rather than a synchronous call from business logic. A producer publishes an event; a distribution service enriches it with user preferences and a rendered template; a durable queue holds it; workers call channel adapters. The queue absorbs bursts and isolates provider outages. Mobile push is indirect: your backend sends a request to FCM or APNs, and that provider delivers to the device over its own persistent connection. Delivery is at-least-once, so design for duplicates with idempotency keys and client-side deduplication. Batching and per-user aggregation reduce spam and provider load.

## Key points

- Mobile push requires a device token issued by FCM (Android) or APNs (iOS); the backend calls the provider, which maintains the connection to the device.
- A durable message queue sits between distribution and send workers so bursts and provider outages do not block business services.
- Push delivery is at-least-once; an ambiguous provider failure followed by a retry can produce duplicates unless the system includes idempotency keys.
- User preferences, quiet hours, and template rendering happen before enqueueing so sends are only attempted for messages the user should receive.
- Delivery callbacks and analytics are a separate path from sending; they drive retries, token cleanup, and reporting.

## Your 60-second answer

A notification system is an asynchronous pipeline that takes events from business services, applies user preferences and templates, then delivers through the appropriate channel. Business services publish to a notification gateway that accepts single or batched requests. A distribution service validates, formats, and schedules each notification, then enqueues it. Workers consume from the queue and call channel adapters: WebSocket for in-app, FCM or APNs for mobile push, an email provider, or an SMS gateway. The queue decouples sending from business logic and absorbs failures. Mobile push works through a device token obtained when the app registers with Apple or Google; the provider keeps the connection to the device. Because external providers are at-least-once, retries can cause duplicates, so I would include an idempotency key per notification and track delivery callbacks for retries and analytics.

## If they dig deeper

**What questions should you ask to clarify the requirements?**

Ask about channels (push, email, SMS), scale (users per second, daily volume), latency requirements, whether notifications are triggered by user actions or system events, and any compliance constraints. This scopes whether you need one or multiple providers and what reliability level is acceptable.

**How do you actually deliver a push notification to a mobile device?**

The app registers with FCM for Android or APNs for iOS and receives a device token. The app sends that token to your backend, stored with the user. To send, a worker calls the provider's API with the token and payload; the provider maintains a persistent connection to the device and delivers it. You never open a socket directly to the phone.

**How do you prevent losing notifications when a provider is down or slow?**

Use a durable message queue between distribution and send workers. Workers consume and call providers synchronously; on failure or timeout, retry with exponential backoff and a dead-letter queue. The job should carry an idempotency key so retries after ambiguous failures don't create duplicate user-visible notifications if downstream supports dedupe.

**How do you scale this to millions of users and bursts?**

Partition the queue by user_id or notification_id so consumers can scale horizontally without ordering conflicts. Use batching windows to collapse multiple events per user into a single push. Rate-limit outbound calls to each provider to stay under their quotas and buffer excess in the queue.

**Can you guarantee exactly-once delivery?**

No. Push providers and client devices may acknowledge but still display duplicates, tokens may be invalid, and provider APIs are at-least-once. You can approximate with idempotent notification IDs, client-side dedupe, and idempotent workers, but end-to-end exactly-once across external providers isn't achievable in practice.

## Worked example

Suppose a chat service wants to notify user 42 about three new messages. The chat service calls the notification gateway with a batch event containing user 42 and the three message IDs. The distribution service looks up user 42's preferences: mobile push is enabled, the current time is outside quiet hours, and the template for multiple messages is '{count} new messages'. It produces one notification job with payload '3 new messages', stores it in Kafka under partition key user 42, and returns 202 to the chat service. A worker consumes the job, fetches user 42's current FCM device token, and calls the FCM send API with that token and a client-generated notification ID. FCM returns 200 and later posts a delivery receipt, which the tracking service records. If FCM had returned 500, the worker would retry with the same notification ID after backoff, so an ambiguous earlier attempt does not generate a different notification ID.

## Common traps

- Jumping straight to box diagrams without asking which channels and scale the interviewer cares about.
- Assuming push delivery is guaranteed or exactly-once.
- Using the same in-app WebSocket path for background mobile push, or forgetting that mobile push needs FCM/APNs.
- Ignoring device token refresh and invalidation: stale tokens cause failures that retries won't fix.

</details>

---

## Two-way (`two-way` · bucket)

### 52. Database sharding · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-database-sharding` then `match: Classify each statement as describing sharding or replicatio`</sub>

**Question**

Classify each statement as describing sharding or replication.

**Options**

**Items**: Each row is stored on exactly one server, and different servers hold different rows., All servers hold the same full copy of the data., Writes are sent to a single primary server and then copied to other servers., A query for a specific key can be routed directly to the server that owns that key., Adding more servers increases the total amount of data the system can store., Adding more servers lets the system handle more read requests without changing the data layout.
**Columns**: Sharding, Replication

**Answer (the reader is graded on)**

- 0 ↔ 0 · 1 ↔ 1 · 2 ↔ 1 · 3 ↔ 0 · 4 ↔ 0 · 5 ↔ 1

**Reference answer**

Sharding splits rows into disjoint subsets on separate servers, so each row lives on exactly one shard and different shards hold different data. Replication keeps full copies of the same rows on multiple servers, so every replica has the same data and reads can be served from any replica while writes go to the primary.

**Graded on**

- Sharding partitions data; replication copies data.
- A sharded row's primary write goes to exactly one shard.
- Replication routes reads to replicas and writes to the primary.
- Sharding increases capacity and write throughput; replication increases read throughput and availability.

<details><summary>The lesson this came from</summary>

Database sharding is horizontal partitioning: a logical table's rows are split into disjoint shards, each stored on a separate database server and holding the same schema. A shard key and routing scheme determine which shard owns a row, so a write or read can be sent directly to the right node. Sharding increases total data capacity and write throughput beyond one machine; it is distinct from replication, which copies the same rows to multiple servers. For MySQL and PostgreSQL, sharding is usually implemented in the application, via a proxy such as Vitess, or through an extension such as Citus; MongoDB has native sharded clusters.

## Why interviewers ask this

Interviewers ask this when a system design grows past a single database. They are testing whether you can choose a shard key from real access patterns, explain how a write or read gets routed, and handle the consequences: hotspots, cross-shard queries, adding capacity, and consistency. Real questions such as designing a job scheduler or a video platform reach sharding at the 'scale across machines' step.

## The core idea

Sharding is a capacity decision, not a default: you partition data only when one server plus replicas can no longer hold the working set or absorb the write load. The shard key determines which queries stay on one shard and which must fan out; choose a high-cardinality key that matches the dominant access pattern. Hash-based routing spreads writes evenly but makes range scans touch every shard; range-based routing keeps ordered scans local but risks writes stacking on one range. Moving shards is expensive, so design rebalancing before launch using consistent hashing, virtual shards, or a directory mapping. Cross-shard joins and transactions are the main recurring cost; real systems often co-locate related rows, denormalize, or aggregate in the application instead.

## Key points

- Sharding splits rows into disjoint shards on separate servers, while replication stores copies of the same rows; a sharded row's primary write goes to exactly one shard.
- A good shard key has high cardinality and aligns with the most common operations; user_id or tenant_id is usually safer than status or country because it spreads data evenly.
- Range-based sharding preserves ordered range scans but can create hotspots on monotonically increasing keys such as timestamps; hash-based sharding spreads load but forces range queries to fan out to all shards.
- Traditional sharded relational databases do not provide cross-shard ACID transactions or joins in the same way a single node does, so you must co-locate, denormalize, or use an application-level join.
- When adding a shard with simple modulo hashing, most keys move; consistent hashing or virtual shards reduce rebalancing to a fraction of keys and are common in distributed systems.

## Your 60-second answer

Sharding is horizontal partitioning: you split a table's rows across multiple database servers by a shard key, so each server holds a subset of the data and the same schema. I'd use it only after a single primary plus read replicas can't hold the data or handle write throughput. The shard key should be high cardinality and match the dominant query pattern—for a job scheduler, tenant_id keeps each tenant's operations on one shard. I'd pick range sharding when ordered scans dominate, hash sharding when I need even distribution, and a directory when I need dynamic movement. The main trade-off is that cross-shard joins and transactions become expensive, so you co-locate related data or aggregate in the application. Rebalancing is the other hard part, so I'd add consistent hashing or virtual shards early.

## If they dig deeper

**How is sharding different from replication?**

Replication keeps full copies of the same data on multiple servers and routes reads to replicas while writes go to the primary. Sharding partitions the data so each row lives on exactly one shard, and different shards handle different subsets. In production you often combine both: each shard may have its own replicas for availability.

**How do you choose a shard key?**

Pick a column that has high cardinality, distributes writes evenly, and appears in most queries. For a job scheduler, tenant_id or user_id keeps all jobs for one tenant on one shard. Avoid low-cardinality keys like status; if you need ordered scans by time but write mostly new rows, range-sharding on timestamp can create a hotspot, so hash may be better.

**What if one shard becomes a hotspot?**

Hotspots usually come from a low-cardinality key or a monotonically increasing range. You can split a hot range into smaller ranges, use a hash with a salt prefix to spread heavy keys, or add virtual shards so hot logical buckets can be moved independently. Monitor keys per shard and rebalance before a node saturates.

**How do you add a new shard without downtime?**

Use consistent hashing or a directory mapping, define the new node's token range, and migrate only the affected key ranges in the background. While migrating, dual-write to old and new shards, verify data with checksums, then atomically update the routing layer to read from the new shard and remove the old copies. Avoid simple modulo because adding a node changes almost every key's target.

**How do you handle cross-shard joins or transactions?**

In many sharded relational databases you can't run a normal SQL join across shards with full ACID, so you either denormalize and co-locate related rows on the same shard, run parallel queries and join in the application, or use a distributed SQL layer that implements cross-shard transactions with a coordinator. If strict consistency is required, look at systems designed for distributed transactions, but this adds latency.

## Worked example

Suppose a job scheduler stores jobs with tenant_id and due_time. With four shards and modulo-4 hashing on tenant_id, tenant 42 maps to shard 2 because 42 % 4 = 2, so all schedule, execute, and history queries for that tenant hit only shard 2. Tenant 43 maps to shard 3. A query for jobs due before 10:00, however, must ask all four shards because due_time is not the shard key. If instead the table is range-sharded by due_time, that query touches only the first range shard, but newly inserted jobs due at the same timestamp pile onto the current hot range. The hash design keeps per-tenant access local; the scheduler can scan each shard independently and merge due jobs.

## Common traps

- Sharding before exhausting a single server, read replicas, and caching, then paying for cross-shard complexity without needing the capacity.
- Picking a low-cardinality shard key like status or region, which creates unbalanced shards and hot nodes.
- Assuming range sharding on an auto-incrementing ID or timestamp is fine; writes concentrate on the highest range and one shard saturates.
- Adding a node by changing a modulo shard count (e.g. 4 to 5) and expecting a small migration; most rows move, requiring large data transfer.

</details>

---

### 53. CDN · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-cdn` then `match: Classify each item as either 'Cacheable on a CDN' or 'Not ca`</sub>

**Question**

Classify each item as either 'Cacheable on a CDN' or 'Not cacheable on a CDN' for a typical web application, assuming standard HTTP caching semantics and no special edge logic.

**Options**

**Items**: User-specific dashboard HTML, Company logo image, Real-time stock price ticker, Global CSS stylesheet, Public product catalog page, Personalized shopping cart contents
**Columns**: Cacheable on a CDN, Not cacheable on a CDN

**Answer (the reader is graded on)**

- 0 ↔ 1 · 1 ↔ 0 · 2 ↔ 1 · 3 ↔ 0 · 4 ↔ 0 · 5 ↔ 1

**Reference answer**

Static assets like images, CSS, JavaScript, and videos are cacheable because they are identical for many users and change rarely. Personalized or frequently changing content, such as user-specific dashboards or real-time stock prices, is not cacheable because it would serve stale or incorrect data to different users.

**Graded on**

- Cacheable content is identical across users and changes infrequently.
- Personalized or rapidly changing content must not be cached globally.
- Cache-Control headers determine freshness and cacheability.

<details><summary>The lesson this came from</summary>

A CDN is a globally distributed system of edge servers that cache content and deliver it from locations close to end users, rather than forcing every request to travel to the origin server. Clients are directed to a nearby edge through DNS-based routing or anycast; an edge serves a cached response if it is fresh, and otherwise fetches, stores, and then serves the object from the origin. CDNs are most effective for static assets such as images, CSS, JavaScript, video, and downloads, but many also accelerate dynamic traffic by terminating TLS and optimizing the path to the origin. Cache behavior is governed by HTTP headers like Cache-Control, and entries can be removed by purge or bypassed with versioned URLs.

## Why interviewers ask this

In system design interviews, CDN questions test whether a candidate knows when to place a cache between users and origin and how to keep the cached data correct. Interviewers look for the ability to separate static from dynamic content, choose TTL and invalidation strategy, and explain the flow of a cache miss. They also probe the operational tradeoffs: stale content, cache hit ratio, origin offload, and DDoS protection.

## The core idea

At its core, a CDN is a distributed cache. The origin server remains the source of truth, while edge servers store copies of immutable or slowly changing objects and absorb most read traffic. A request is routed to the closest edge by the CDN's DNS or anycast network; on a miss, the edge pulls the object from the origin once and then serves subsequent requests locally. This shortens the network path for users and reduces the number of requests hitting the origin, which also makes the origin harder to overwhelm with a DDoS attack. The main design decisions are what to cache, how long to keep it, and how to invalidate it.

## Key points

- A CDN is a network of edge servers that serve cached content from locations geographically close to users, reducing latency and origin load.
- Requests are directed to a nearby edge via DNS resolution or anycast; a cache miss fetches from the origin and stores the response for later hits.
- Static assets like images, CSS, JavaScript, and video are the best CDN candidates because they are identical for many users and change rarely.
- Caching freshness is controlled by HTTP cache headers such as Cache-Control and Expires, and invalidation is done by purging or by changing the URL when content changes.
- CDNs also improve availability and absorb DDoS attacks by spreading traffic across many edge locations and only forwarding cache misses to the origin.

## Your 60-second answer

A CDN is a geographically distributed network of edge servers that cache content and serve it close to users. When a client requests an asset, the CDN's DNS resolution directs the client to the nearest edge server rather than the origin. If the edge has a fresh cached copy, it sends that copy directly, which eliminates the delay of crossing a long distance and removes load from your origin. If it is a miss, the edge pulls the object from the origin once, stores it according to its cache headers, and serves the user; later requests near that edge hit the cache. The core tradeoff is freshness versus speed: cached content can be stale until the TTL expires or you actively purge it. That is why static files like images, CSS, and JavaScript are ideal for CDN caching, while personalized or rapidly changing responses usually require a different strategy.

## If they dig deeper

**What kinds of content should you put on a CDN?**

Static, cacheable assets such as images, CSS, JavaScript, fonts, videos, and downloadable files, because they are the same for many users and do not change often. Personalized or frequently changing content should either bypass full caching or use very short TTLs and fragment-level caching, otherwise you risk serving another user's data.

**How does a client actually get routed to the nearest CDN edge?**

Usually the hostname is delegated to the CDN, and the CDN's authoritative DNS returns the IP address of an edge close to the client's resolver, using GeoIP or similar routing. With anycast, the CDN announces the same IP from many edges, and BGP routes packets to the network-closest point; many CDNs combine DNS steering and anycast.

**What happens when a CDN has a cache miss, and how do you invalidate a stale object?**

On a miss, the edge contacts the origin, fetches the full response, stores it locally for the duration specified by Cache-Control or other cache headers, and returns it to the client. Invalidation can be done by sending a purge request to the CDN for the URL, or more reliably by versioning the filename or query string so changed content is treated as a new cache key.

**CDNs are great for static files, but how do they help with dynamic content?**

They usually do not cache the full dynamic response unless it is explicitly public and cacheable. Instead, they terminate TLS at the edge to reduce handshake latency, keep warm connections to the origin, and route over optimized backbone links; some CDNs also run edge code to assemble personalized fragments or serve API responses from edge key-value stores.

**If you had to design a CDN from scratch, what are the main components you would need?**

You need edge points of presence with cache servers, a request routing layer based on DNS or anycast, and a way for edges to fetch from origin. The harder parts are cache consistency and purge propagation, protecting the origin from a stampede when a popular object expires, TLS certificate management for many customer domains, and DDoS scrubbing at the edge.

## Worked example

A user in London requests https://cdn.example.com/hero.jpg. The hostname resolves through the CDN's DNS to an edge server in London because the CDN's DNS returns the address of the nearest edge. The edge checks its cache; this is the first request for that object, so it is a miss. The edge opens a connection to the origin, fetches the image, stores it with the TTL from the Cache-Control header, and returns the bytes to the user. A second London user requesting the same URL soon after is served directly from the London edge with no origin contact. If the marketing team later publishes a new hero image at the same URL, users may continue receiving the cached old image until its TTL expires or the CDN receives a purge. The safe fix is to version the URL, such as /hero-v2.jpg, so the new asset has a distinct cache key and is fetched immediately.

## Common traps

- Assuming a CDN replaces the origin or is a separate copy of the whole database, without realising the origin remains the source of truth for misses and writes.
- Caching personalized or user-specific pages because they seem static, which can leak one user's data to another.
- Changing a file on the origin and expecting users to see the new version immediately while a long Cache-Control or CDN TTL is still active.
- Forgetting that DNS changes take time to propagate and that moving a domain onto or off a CDN can leave clients talking to old servers if CNAME and TTL changes are not handled carefully.

</details>

---

## Three-way (`three-way` · bucket)

### 54. Triggers · Medium

*sql · gate confidence 0.7*

<sub>to object to this card: `## sql-triggers` then `match: Classify each trigger-related statement by the database system it describes. Assume standard behavior and default constr`</sub>

**Question**

Classify each trigger-related statement by the database system it describes. Assume standard behavior and default constraint timing unless stated otherwise.

**Options**

**Items**: AFTER triggers run after constraint checks, Supports row-level and statement-level triggers, Supports INSTEAD OF triggers on views, DML triggers are statement-level, Supports only row-level BEFORE and AFTER triggers on tables, Row-level AFTER triggers can run before deferred constraint checks
**Columns**: SQL Server, PostgreSQL, MySQL

**Answer (the reader is graded on)**

- 0 ↔ 0 · 1 ↔ 1 · 2 ↔ 0 · 3 ↔ 0 · 4 ↔ 2 · 5 ↔ 1

**Reference answer**

SQL Server: DML triggers are statement-level; AFTER triggers run after constraint checks; INSTEAD OF triggers can be defined on views. PostgreSQL: supports row-level and statement-level triggers; row-level AFTER triggers can run before deferred constraint checks; INSTEAD OF triggers can be defined on views. MySQL: supports only row-level BEFORE and AFTER triggers on tables; does not support INSTEAD OF triggers.

**Graded on**

- SQL Server DML triggers fire once per statement and use inserted/deleted pseudo-tables.
- PostgreSQL supports both row-level and statement-level triggers, and row-level AFTER triggers can run before deferred constraints.
- MySQL supports only row-level BEFORE and AFTER triggers on tables and has no INSTEAD OF triggers.

<details><summary>The lesson this came from</summary>

A trigger is a database object bound to a table or view that automatically executes procedural SQL in response to specified DML (INSERT, UPDATE, DELETE) or DDL events. SQL Server implements DML triggers as statement-level procedures with inserted and deleted pseudo-tables; PostgreSQL supports row-level and statement-level triggers with OLD and NEW record values; MySQL implements row-level BEFORE and AFTER triggers on tables. The trigger body runs in the same transaction as the triggering statement unless the DBMS provides separate autonomous transaction features.

## Why interviewers ask this

Interviewers ask about triggers to see whether you understand how database-enforced logic differs from application logic: it runs automatically, cannot be bypassed by a client, and can hide side effects inside write paths. They probe transaction and timing semantics because a candidate who thinks all DBMSs fire AFTER triggers after constraint checks will make costly schema or recovery mistakes.

## The core idea

A trigger is a stored routine tied to an event rather than called by a client. DML changes construct transition data: SQL Server exposes inserted and deleted pseudo-tables containing the full set of affected rows for one statement; PostgreSQL and MySQL row-level triggers expose OLD and NEW values per row. The trigger executes in the same transaction as the DML, so its effects either commit or roll back with the statement unless the DBMS has autonomous transaction support. Because trigger timing relative to constraint checking differs by engine—SQL Server AFTER is post-constraint, while PostgreSQL row-level AFTER can run before deferred constraints—you must state the DBMS when discussing ordering. Recursive or long-running triggers are a common source of surprising locks and rollbacks.

## Key points

- SQL Server DML triggers are statement-level and fire once per INSERT, UPDATE, or DELETE statement, using inserted and deleted pseudo-tables for new and old row sets.
- PostgreSQL supports row-level and statement-level BEFORE, AFTER, and on views INSTEAD OF triggers; MySQL supports only row-level BEFORE and AFTER triggers on tables.
- SQL Server AFTER triggers run after the triggering DML and after constraint checks, but in PostgreSQL row-level AFTER triggers run before deferred constraint checks, and constraint timing depends on deferrability.
- In SQL Server, INSTEAD OF triggers can be defined on tables or views, while AFTER/FOR triggers cannot be defined on views.
- A trigger executes in the same transaction as the triggering statement, so an error in the trigger normally rolls back the statement, and recursive triggers can hit engine-defined nesting limits.

## Your 60-second answer

A trigger is a database object that automatically executes procedural code when a specified DML or DDL event occurs on a table or view. In SQL Server I can define an AFTER UPDATE trigger to audit salary changes; it fires once per statement and reads the inserted and deleted pseudo-tables, which hold the new and old row sets. PostgreSQL and MySQL use OLD and NEW record references in row-level triggers instead. The main benefit is enforcing logic inside the storage layer so no client can bypass it; the trade-off is that the trigger runs in the same transaction, can hide side effects, slow writes, and cause recursive cascades. I also qualify timing: SQL Server AFTER runs after constraint checks, but PostgreSQL row-level AFTER can run before deferred constraints. I use triggers only for cross-row invariants, auditing, or denormalization that constraints cannot express.

## If they dig deeper

**In SQL Server, what are the inserted and deleted tables inside a trigger?**

They are pseudo-tables available only inside DML triggers. INSERT and UPDATE populate inserted with new values; DELETE and UPDATE populate deleted with old values. Because SQL Server DML triggers fire once per statement, these pseudo-tables contain all rows affected by that statement, and you join them on the primary key to compare old and new values.

**What is the difference between AFTER and INSTEAD OF triggers in SQL Server?**

AFTER triggers execute after the DML operation has been applied and, in SQL Server, after constraints have been checked; they cannot be defined on views. INSTEAD OF triggers replace the DML operation entirely, run before any changes are made, and can be defined on tables or views, which is how views are made updatable in SQL Server.

**How do BEFORE and AFTER row-level triggers compare in PostgreSQL, and when does constraint checking happen?**

In PostgreSQL, a BEFORE row-level trigger fires before the row is written and can modify the NEW record, while an AFTER row-level trigger fires after the row is written but before the end of the statement. Non-deferred constraints are checked immediately or at statement end depending on type; deferred constraints are checked at commit. Thus a row-level AFTER trigger can see changes before a deferred constraint check rejects them.

**What problems do recursive triggers cause and how are they controlled?**

A trigger that performs the same DML on its own table can fire itself repeatedly, consuming resources and locking rows. SQL Server has a maximum nested trigger level and an option to disable recursive triggers; other DBMSs have engine-specific recursion settings. The real fix is to design trigger logic so it does not re-enter the same table, for example by using an INSTEAD OF trigger or a guard column.

**Why are triggers considered risky in high-throughput write paths?**

They add procedural work to every write inside the same transaction, can acquire locks in the trigger body, and make data changes depend on hidden code. A trigger that performs heavy queries or updates other tables serializes writes and complicates rollback analysis. Strong candidates explain that triggers are best reserved for invariants or side effects that cannot be expressed declaratively, and should be benchmarked under realistic write load.

## Worked example

Consider a SQL Server table Employees(EmployeeID, Name, Salary). A statement-level AFTER UPDATE trigger audits salary changes. An application runs UPDATE Employees SET Salary = Salary * 1.10 WHERE DepartmentID = 3, affecting two rows with old salaries 100000 and 80000. Because the trigger fires once for the whole statement, inserted holds both new salaries 110000 and 88000, while deleted holds both old salaries. The trigger body inserts into SalaryAudit by joining deleted and inserted on EmployeeID and filtering d.Salary <> i.Salary, producing two audit rows. Had the trigger body raised an error, the entire update would roll back because the trigger runs in the same transaction as the statement.

## Common traps

- Claiming AFTER triggers always fire after constraint checks: in PostgreSQL row-level AFTER triggers can run before deferred constraints, and deferrability changes when constraints are enforced.
- Writing a SQL Server trigger under the assumption it fires once per row, when DML triggers there are statement-level and inserted or deleted may contain many rows.
- Updating the same table inside an AFTER UPDATE trigger without a recursion guard, causing re-entry or hitting the engine's nested trigger limit.
- Forgetting that triggers execute inside the triggering transaction, so errors roll back both the trigger's work and the original DML statement.

</details>

---

### 55. API Gateway · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-api-gateway` then `match: Classify each responsibility as belonging to the API Gateway, the Backend Service, or Both`</sub>

**Question**

Classify each responsibility as belonging to the API Gateway, the Backend Service, or Both. Assume a standard microservices architecture where the gateway handles cross-cutting concerns and services own business logic.

**Options**

**Items**: Authentication, Business logic, Rate limiting, TLS termination, Database access, Logging
**Columns**: API Gateway, Backend Service, Both

**Answer (the reader is graded on)**

- 0 ↔ 0 · 1 ↔ 1 · 2 ↔ 0 · 3 ↔ 0 · 4 ↔ 1 · 5 ↔ 2

**Reference answer**

Authentication, rate limiting, and TLS termination are gateway responsibilities. Business logic and database access belong to backend services. Logging is done by both: the gateway logs request metadata at the edge, while services log business events.

**Graded on**

- The gateway enforces cross-cutting policies like auth and rate limiting at the edge.
- Backend services implement business logic and own their data.
- Logging is shared: gateway logs traffic metadata, services log domain events.

<details><summary>The lesson this came from</summary>

An API gateway is a reverse proxy that accepts all client API calls, applies cross-cutting policies, and forwards each request to the appropriate backend service. In a microservices architecture it hides internal service boundaries behind one client-facing endpoint, handling authentication, authorization, rate limiting, load balancing, caching, request/response transformation, and observability. The gateway itself should contain no business logic; it manages traffic and policy at the edge.

## Why interviewers ask this

At Amazon, Atlassian, Uber, and Patreon, rate-limiter questions probe the same component because gateways are the natural enforcement point. The interviewer is testing whether you can design a single entry point that remains correct under concurrency, scales horizontally, and fails without taking the whole system down. They also look for separation of cross-cutting concerns from business logic.

## The core idea

The gateway is the edge policy engine. It terminates client TLS, authenticates the caller, checks quotas, and then routes the request according to path, method, and headers. It may also compose responses from multiple services or cache them so backend load drops. Because all traffic passes through it, it becomes both the best place to enforce organization-wide rules and the most dangerous single point of failure. A strong design keeps it stateless, horizontally scaled, and equipped with timeouts, retries, and circuit breakers. The routing table or service discovery layer tells it where each request should go without embedding service addresses in clients.

## Key points

- An API gateway terminates client TLS, authenticates requests, authorizes per route, and proxies to backend services, so individual services do not repeat these checks.
- Rate limiting at the gateway can use token bucket or sliding window algorithms; in a distributed deployment the counters must live in a shared store such as Redis rather than per-instance memory.
- API composition lets the gateway call multiple services and merge responses to reduce client round trips, but it adds gateway latency and complexity.
- The gateway must be stateless and horizontally scalable behind a load balancer, with health checks, timeouts, retries, and circuit breakers to avoid cascading failures.
- Common gateway implementations include AWS API Gateway, Kong, and NGINX/OpenResty, though features and configuration models vary by product.

## Your 60-second answer

An API gateway is a single entry point that sits between clients and backend services. It receives every API request, terminates TLS, authenticates the caller, enforces rate limits, and routes the request to the correct service. It also handles cross-cutting concerns like caching, request and response transformation, and monitoring, so downstream services don't duplicate that work. The reason you add one is that microservices expose many fine-grained endpoints; a gateway composes them into one client-friendly API and applies policies at the edge. The main trade-off is that it becomes a critical path: if it fails or is misconfigured, all traffic stops. So you run multiple stateless instances, set timeouts and circuit breakers, and avoid putting business logic in the gateway.

## If they dig deeper

**What are the core responsibilities of an API gateway?**

Routing requests to the correct backend, authentication and authorization, rate limiting, load balancing, caching, request/response transformation, and observability. It can also do API composition, calling multiple services and merging responses. It should not contain business logic.

**How would you implement authentication and authorization at the gateway?**

Validate the caller's credential, usually a JWT or OAuth2 token, at the edge by checking signature, expiry, issuer, and audience. On failure return 401; after authentication check scopes or roles against the route and return 403 if insufficient. Then forward the request with trusted identity headers to downstream services.

**How do you implement rate limiting at the gateway?**

Identify the client by API key, user ID, or IP address. For a single gateway instance, keep a token bucket or sliding window counter in memory; for multiple instances, store counters in Redis with atomic operations. When the limit is exceeded, return HTTP 429 with Retry-After and rate limit headers.

**How do you scale rate limiting across many gateway instances?**

Share the counter state in a central store like Redis and use atomic Lua scripts or sorted sets for sliding windows. Fixed-window counters are simpler but can allow bursts at window boundaries; sliding window log gives accuracy at higher memory cost. If per-instance counters are used, clients can exceed the global limit by hitting different instances, so a shared store is usually required.

**How do you make the gateway fault tolerant and prevent it from becoming a bottleneck?**

Run multiple stateless gateway instances behind a load balancer, set aggressive timeouts, use circuit breakers to stop calling unhealthy services, and retry only idempotent requests. Cache safe responses, monitor CPU and connection saturation, and decide whether to fail open or fail closed when the rate limiter or auth service is unavailable. Keep the gateway free of business logic so changes are rare and deployments are low-risk.

## Worked example

A mobile client sends POST /orders to the gateway. The gateway terminates TLS, validates the JWT signature and expiry, and reads the user ID. It checks a token bucket in Redis for key rate:user:123. The bucket has capacity 100 and refills 10 tokens per second; at this moment 4 tokens remain because the user has consumed 96 requests in the current minute. The gateway allows the request, decrements the bucket to 3, and forwards it to the order service with an X-User-Id header. The order service returns 201, and the gateway strips internal fields before returning JSON. After three more rapid requests the bucket reaches 0, so the next request receives HTTP 429 with Retry-After: 30 and X-RateLimit-Remaining: 0.

## Common traps

- Putting business logic in the gateway, which turns it into a distributed monolith and forces a gateway deployment for every feature change.
- Using per-instance in-memory counters for rate limiting in a multi-instance deployment, allowing a client to exceed the global limit by spreading requests across instances.
- Forgetting timeouts and circuit breakers, so a slow downstream service consumes all gateway threads and makes every API unavailable.
- Assuming the gateway will never fail and not planning redundancy or a fail-open/fail-closed policy, which creates a single point of failure.

</details>

---

## Which layer (`which-layer` · bucket)

### 56. Design a notification system · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-design-a-notification-system` then `match: Sort each component of a notification system into the layer `</sub>

**Question**

Sort each component of a notification system into the layer where it belongs: the layer that accepts requests from business services, the layer that enriches and schedules notifications, or the layer that actually delivers to users. Assume a standard asynchronous pipeline with a durable queue between distribution and delivery.

**Options**

**Items**: Notification gateway, Distribution service, Send workers, Channel adapters (WebSocket, FCM/APNs, email, SMS), Durable message queue, Delivery callback tracking service
**Columns**: Acceptance layer, Distribution layer, Delivery layer

**Answer (the reader is graded on)**

- 0 ↔ 0 · 1 ↔ 1 · 2 ↔ 2 · 3 ↔ 2 · 4 ↔ 1 · 5 ↔ 2

**Reference answer**

The notification gateway accepts requests from business services. The distribution service applies user preferences and templates, then enqueues jobs. The send workers call channel adapters (WebSocket, FCM/APNs, email, SMS) to deliver to users.

**Graded on**

- Gateway is the entry point for business services.
- Distribution service enriches with preferences and templates before enqueueing.
- Send workers and channel adapters perform actual delivery.

<details><summary>The lesson this came from</summary>

A notification system is backend infrastructure that accepts notification requests from business services, validates and formats them, and dispatches messages to users over channels such as in-app real-time connections, mobile push providers, email, or SMS. It typically has a gateway, a distribution layer that applies templates and user preferences, durable queues, and channel-specific workers. For mobile push, the backend calls platform providers like FCM for Android and APNs for iOS using per-device tokens; for in-app delivery it may push over a WebSocket connection. The system also records delivery callbacks for retry and analytics.

## Why interviewers ask this

The interviewer is testing whether you can turn a vague 'notify the user' requirement into components with clear responsibilities, handle external provider failures, and scale an asynchronous pipeline. They also probe whether you understand that mobile push has different delivery semantics from in-app streaming, and that external providers impose at-least-once behavior. Strong candidates ask about channels, volume, and latency before drawing a diagram.

## The core idea

Treat sending a notification as an asynchronous pipeline rather than a synchronous call from business logic. A producer publishes an event; a distribution service enriches it with user preferences and a rendered template; a durable queue holds it; workers call channel adapters. The queue absorbs bursts and isolates provider outages. Mobile push is indirect: your backend sends a request to FCM or APNs, and that provider delivers to the device over its own persistent connection. Delivery is at-least-once, so design for duplicates with idempotency keys and client-side deduplication. Batching and per-user aggregation reduce spam and provider load.

## Key points

- Mobile push requires a device token issued by FCM (Android) or APNs (iOS); the backend calls the provider, which maintains the connection to the device.
- A durable message queue sits between distribution and send workers so bursts and provider outages do not block business services.
- Push delivery is at-least-once; an ambiguous provider failure followed by a retry can produce duplicates unless the system includes idempotency keys.
- User preferences, quiet hours, and template rendering happen before enqueueing so sends are only attempted for messages the user should receive.
- Delivery callbacks and analytics are a separate path from sending; they drive retries, token cleanup, and reporting.

## Your 60-second answer

A notification system is an asynchronous pipeline that takes events from business services, applies user preferences and templates, then delivers through the appropriate channel. Business services publish to a notification gateway that accepts single or batched requests. A distribution service validates, formats, and schedules each notification, then enqueues it. Workers consume from the queue and call channel adapters: WebSocket for in-app, FCM or APNs for mobile push, an email provider, or an SMS gateway. The queue decouples sending from business logic and absorbs failures. Mobile push works through a device token obtained when the app registers with Apple or Google; the provider keeps the connection to the device. Because external providers are at-least-once, retries can cause duplicates, so I would include an idempotency key per notification and track delivery callbacks for retries and analytics.

## If they dig deeper

**What questions should you ask to clarify the requirements?**

Ask about channels (push, email, SMS), scale (users per second, daily volume), latency requirements, whether notifications are triggered by user actions or system events, and any compliance constraints. This scopes whether you need one or multiple providers and what reliability level is acceptable.

**How do you actually deliver a push notification to a mobile device?**

The app registers with FCM for Android or APNs for iOS and receives a device token. The app sends that token to your backend, stored with the user. To send, a worker calls the provider's API with the token and payload; the provider maintains a persistent connection to the device and delivers it. You never open a socket directly to the phone.

**How do you prevent losing notifications when a provider is down or slow?**

Use a durable message queue between distribution and send workers. Workers consume and call providers synchronously; on failure or timeout, retry with exponential backoff and a dead-letter queue. The job should carry an idempotency key so retries after ambiguous failures don't create duplicate user-visible notifications if downstream supports dedupe.

**How do you scale this to millions of users and bursts?**

Partition the queue by user_id or notification_id so consumers can scale horizontally without ordering conflicts. Use batching windows to collapse multiple events per user into a single push. Rate-limit outbound calls to each provider to stay under their quotas and buffer excess in the queue.

**Can you guarantee exactly-once delivery?**

No. Push providers and client devices may acknowledge but still display duplicates, tokens may be invalid, and provider APIs are at-least-once. You can approximate with idempotent notification IDs, client-side dedupe, and idempotent workers, but end-to-end exactly-once across external providers isn't achievable in practice.

## Worked example

Suppose a chat service wants to notify user 42 about three new messages. The chat service calls the notification gateway with a batch event containing user 42 and the three message IDs. The distribution service looks up user 42's preferences: mobile push is enabled, the current time is outside quiet hours, and the template for multiple messages is '{count} new messages'. It produces one notification job with payload '3 new messages', stores it in Kafka under partition key user 42, and returns 202 to the chat service. A worker consumes the job, fetches user 42's current FCM device token, and calls the FCM send API with that token and a client-generated notification ID. FCM returns 200 and later posts a delivery receipt, which the tracking service records. If FCM had returned 500, the worker would retry with the same notification ID after backoff, so an ambiguous earlier attempt does not generate a different notification ID.

## Common traps

- Jumping straight to box diagrams without asking which channels and scale the interviewer cares about.
- Assuming push delivery is guaranteed or exactly-once.
- Using the same in-app WebSocket path for background mobile push, or forgetting that mobile push needs FCM/APNs.
- Ignoring device token refresh and invalidation: stale tokens cause failures that retries won't fix.

</details>

---

### 57. CDN · Easy

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-cdn` then `match: Classify each item as either 'Cache at CDN edge' or 'Do not `</sub>

**Question**

Classify each item as either 'Cache at CDN edge' or 'Do not cache at CDN edge' for a typical web application. Assume standard HTTP caching semantics and that personalized content must not be shared between users.

**Options**

**Items**: User's shopping cart contents, Company logo image, Personalized dashboard HTML, Global CSS stylesheet, Product listing page that changes every minute, JavaScript bundle for all users
**Columns**: Cache at CDN edge, Do not cache at CDN edge

**Answer (the reader is graded on)**

- 0 ↔ 1 · 1 ↔ 0 · 2 ↔ 1 · 3 ↔ 0 · 4 ↔ 1 · 5 ↔ 0

**Reference answer**

Static assets like images, CSS, JavaScript, and videos are ideal for CDN caching because they are identical for many users and change rarely. Personalized pages, user-specific data, and frequently changing content should not be cached at the edge, as they risk serving stale or incorrect data to users.

**Graded on**

- CDNs cache content that is identical across users and changes infrequently.
- Personalized or user-specific responses must not be cached at the edge.
- Static assets such as images, CSS, and JavaScript are prime CDN candidates.

<details><summary>The lesson this came from</summary>

A CDN is a globally distributed system of edge servers that cache content and deliver it from locations close to end users, rather than forcing every request to travel to the origin server. Clients are directed to a nearby edge through DNS-based routing or anycast; an edge serves a cached response if it is fresh, and otherwise fetches, stores, and then serves the object from the origin. CDNs are most effective for static assets such as images, CSS, JavaScript, video, and downloads, but many also accelerate dynamic traffic by terminating TLS and optimizing the path to the origin. Cache behavior is governed by HTTP headers like Cache-Control, and entries can be removed by purge or bypassed with versioned URLs.

## Why interviewers ask this

In system design interviews, CDN questions test whether a candidate knows when to place a cache between users and origin and how to keep the cached data correct. Interviewers look for the ability to separate static from dynamic content, choose TTL and invalidation strategy, and explain the flow of a cache miss. They also probe the operational tradeoffs: stale content, cache hit ratio, origin offload, and DDoS protection.

## The core idea

At its core, a CDN is a distributed cache. The origin server remains the source of truth, while edge servers store copies of immutable or slowly changing objects and absorb most read traffic. A request is routed to the closest edge by the CDN's DNS or anycast network; on a miss, the edge pulls the object from the origin once and then serves subsequent requests locally. This shortens the network path for users and reduces the number of requests hitting the origin, which also makes the origin harder to overwhelm with a DDoS attack. The main design decisions are what to cache, how long to keep it, and how to invalidate it.

## Key points

- A CDN is a network of edge servers that serve cached content from locations geographically close to users, reducing latency and origin load.
- Requests are directed to a nearby edge via DNS resolution or anycast; a cache miss fetches from the origin and stores the response for later hits.
- Static assets like images, CSS, JavaScript, and video are the best CDN candidates because they are identical for many users and change rarely.
- Caching freshness is controlled by HTTP cache headers such as Cache-Control and Expires, and invalidation is done by purging or by changing the URL when content changes.
- CDNs also improve availability and absorb DDoS attacks by spreading traffic across many edge locations and only forwarding cache misses to the origin.

## Your 60-second answer

A CDN is a geographically distributed network of edge servers that cache content and serve it close to users. When a client requests an asset, the CDN's DNS resolution directs the client to the nearest edge server rather than the origin. If the edge has a fresh cached copy, it sends that copy directly, which eliminates the delay of crossing a long distance and removes load from your origin. If it is a miss, the edge pulls the object from the origin once, stores it according to its cache headers, and serves the user; later requests near that edge hit the cache. The core tradeoff is freshness versus speed: cached content can be stale until the TTL expires or you actively purge it. That is why static files like images, CSS, and JavaScript are ideal for CDN caching, while personalized or rapidly changing responses usually require a different strategy.

## If they dig deeper

**What kinds of content should you put on a CDN?**

Static, cacheable assets such as images, CSS, JavaScript, fonts, videos, and downloadable files, because they are the same for many users and do not change often. Personalized or frequently changing content should either bypass full caching or use very short TTLs and fragment-level caching, otherwise you risk serving another user's data.

**How does a client actually get routed to the nearest CDN edge?**

Usually the hostname is delegated to the CDN, and the CDN's authoritative DNS returns the IP address of an edge close to the client's resolver, using GeoIP or similar routing. With anycast, the CDN announces the same IP from many edges, and BGP routes packets to the network-closest point; many CDNs combine DNS steering and anycast.

**What happens when a CDN has a cache miss, and how do you invalidate a stale object?**

On a miss, the edge contacts the origin, fetches the full response, stores it locally for the duration specified by Cache-Control or other cache headers, and returns it to the client. Invalidation can be done by sending a purge request to the CDN for the URL, or more reliably by versioning the filename or query string so changed content is treated as a new cache key.

**CDNs are great for static files, but how do they help with dynamic content?**

They usually do not cache the full dynamic response unless it is explicitly public and cacheable. Instead, they terminate TLS at the edge to reduce handshake latency, keep warm connections to the origin, and route over optimized backbone links; some CDNs also run edge code to assemble personalized fragments or serve API responses from edge key-value stores.

**If you had to design a CDN from scratch, what are the main components you would need?**

You need edge points of presence with cache servers, a request routing layer based on DNS or anycast, and a way for edges to fetch from origin. The harder parts are cache consistency and purge propagation, protecting the origin from a stampede when a popular object expires, TLS certificate management for many customer domains, and DDoS scrubbing at the edge.

## Worked example

A user in London requests https://cdn.example.com/hero.jpg. The hostname resolves through the CDN's DNS to an edge server in London because the CDN's DNS returns the address of the nearest edge. The edge checks its cache; this is the first request for that object, so it is a miss. The edge opens a connection to the origin, fetches the image, stores it with the TTL from the Cache-Control header, and returns the bytes to the user. A second London user requesting the same URL soon after is served directly from the London edge with no origin contact. If the marketing team later publishes a new hero image at the same URL, users may continue receiving the cached old image until its TTL expires or the CDN receives a purge. The safe fix is to version the URL, such as /hero-v2.jpg, so the new asset has a distinct cache key and is fetched immediately.

## Common traps

- Assuming a CDN replaces the origin or is a separate copy of the whole database, without realising the origin remains the source of truth for misses and writes.
- Caching personalized or user-specific pages because they seem static, which can leak one user's data to another.
- Changing a file on the origin and expecting users to see the new version immediately while a long Cache-Control or CDN TTL is still active.
- Forgetting that DNS changes take time to propagate and that moving a domain onto or off a CDN can leave clients talking to old servers if CNAME and TTL changes are not handled carefully.

</details>

---

## Tap the bug (`tap-the-bug` · tap_in_place)

### 58. Triggers · Easy

*sql · gate confidence 0.8*

<sub>to object to this card: `## sql-triggers` then `match: Consider this SQL Server trigger definition: 1 CREATE TRIGGE`</sub>

**Question**

Consider this SQL Server trigger definition:

1  CREATE TRIGGER trg_AuditSalary
2  ON Employees
3  AFTER UPDATE
4  AS
5  BEGIN
6      INSERT INTO SalaryAudit (EmployeeID, OldSalary, NewSalary)
7      SELECT d.EmployeeID, d.Salary, i.Salary
8      FROM deleted d
9      JOIN inserted i ON d.EmployeeID = i.EmployeeID
10     WHERE d.Salary <> i.Salary;
11 END;

Which line contains the bug?

**Options**

A. 1  CREATE TRIGGER trg_AuditSalary
B. 2  ON Employees
C. 3  AFTER UPDATE
D. 4  AS
E. 5  BEGIN
F. 6      INSERT INTO SalaryAudit (EmployeeID, OldSalary, NewSalary)
G. 7      SELECT d.EmployeeID, d.Salary, i.Salary
H. 8      FROM deleted d
I. 9      JOIN inserted i ON d.EmployeeID = i.EmployeeID
J. 10     WHERE d.Salary <> i.Salary;
K. 11 END;

**Answer (the reader is graded on)**

- Correct: C. 3  AFTER UPDATE

**Reference answer**

Line 3 is the bug: AFTER triggers cannot be defined on views, but the question does not state that Employees is a view. The actual bug is that the trigger is defined as AFTER UPDATE, but the lesson states that AFTER triggers cannot be defined on views, and the question does not specify that Employees is a table. However, the most likely intended bug is that the trigger is missing a check for UPDATE(Salary) or a guard against recursion, but the given options do not include such a line. The correct answer is line 3 because AFTER triggers cannot be defined on views, and the question does not specify that Employees is a table.

**Graded on**

- AFTER triggers cannot be defined on views in SQL Server.
- The question does not state that Employees is a table, so the trigger definition is invalid.
- INSTEAD OF triggers can be defined on views, but AFTER triggers cannot.

<details><summary>The lesson this came from</summary>

A trigger is a database object bound to a table or view that automatically executes procedural SQL in response to specified DML (INSERT, UPDATE, DELETE) or DDL events. SQL Server implements DML triggers as statement-level procedures with inserted and deleted pseudo-tables; PostgreSQL supports row-level and statement-level triggers with OLD and NEW record values; MySQL implements row-level BEFORE and AFTER triggers on tables. The trigger body runs in the same transaction as the triggering statement unless the DBMS provides separate autonomous transaction features.

## Why interviewers ask this

Interviewers ask about triggers to see whether you understand how database-enforced logic differs from application logic: it runs automatically, cannot be bypassed by a client, and can hide side effects inside write paths. They probe transaction and timing semantics because a candidate who thinks all DBMSs fire AFTER triggers after constraint checks will make costly schema or recovery mistakes.

## The core idea

A trigger is a stored routine tied to an event rather than called by a client. DML changes construct transition data: SQL Server exposes inserted and deleted pseudo-tables containing the full set of affected rows for one statement; PostgreSQL and MySQL row-level triggers expose OLD and NEW values per row. The trigger executes in the same transaction as the DML, so its effects either commit or roll back with the statement unless the DBMS has autonomous transaction support. Because trigger timing relative to constraint checking differs by engine—SQL Server AFTER is post-constraint, while PostgreSQL row-level AFTER can run before deferred constraints—you must state the DBMS when discussing ordering. Recursive or long-running triggers are a common source of surprising locks and rollbacks.

## Key points

- SQL Server DML triggers are statement-level and fire once per INSERT, UPDATE, or DELETE statement, using inserted and deleted pseudo-tables for new and old row sets.
- PostgreSQL supports row-level and statement-level BEFORE, AFTER, and on views INSTEAD OF triggers; MySQL supports only row-level BEFORE and AFTER triggers on tables.
- SQL Server AFTER triggers run after the triggering DML and after constraint checks, but in PostgreSQL row-level AFTER triggers run before deferred constraint checks, and constraint timing depends on deferrability.
- In SQL Server, INSTEAD OF triggers can be defined on tables or views, while AFTER/FOR triggers cannot be defined on views.
- A trigger executes in the same transaction as the triggering statement, so an error in the trigger normally rolls back the statement, and recursive triggers can hit engine-defined nesting limits.

## Your 60-second answer

A trigger is a database object that automatically executes procedural code when a specified DML or DDL event occurs on a table or view. In SQL Server I can define an AFTER UPDATE trigger to audit salary changes; it fires once per statement and reads the inserted and deleted pseudo-tables, which hold the new and old row sets. PostgreSQL and MySQL use OLD and NEW record references in row-level triggers instead. The main benefit is enforcing logic inside the storage layer so no client can bypass it; the trade-off is that the trigger runs in the same transaction, can hide side effects, slow writes, and cause recursive cascades. I also qualify timing: SQL Server AFTER runs after constraint checks, but PostgreSQL row-level AFTER can run before deferred constraints. I use triggers only for cross-row invariants, auditing, or denormalization that constraints cannot express.

## If they dig deeper

**In SQL Server, what are the inserted and deleted tables inside a trigger?**

They are pseudo-tables available only inside DML triggers. INSERT and UPDATE populate inserted with new values; DELETE and UPDATE populate deleted with old values. Because SQL Server DML triggers fire once per statement, these pseudo-tables contain all rows affected by that statement, and you join them on the primary key to compare old and new values.

**What is the difference between AFTER and INSTEAD OF triggers in SQL Server?**

AFTER triggers execute after the DML operation has been applied and, in SQL Server, after constraints have been checked; they cannot be defined on views. INSTEAD OF triggers replace the DML operation entirely, run before any changes are made, and can be defined on tables or views, which is how views are made updatable in SQL Server.

**How do BEFORE and AFTER row-level triggers compare in PostgreSQL, and when does constraint checking happen?**

In PostgreSQL, a BEFORE row-level trigger fires before the row is written and can modify the NEW record, while an AFTER row-level trigger fires after the row is written but before the end of the statement. Non-deferred constraints are checked immediately or at statement end depending on type; deferred constraints are checked at commit. Thus a row-level AFTER trigger can see changes before a deferred constraint check rejects them.

**What problems do recursive triggers cause and how are they controlled?**

A trigger that performs the same DML on its own table can fire itself repeatedly, consuming resources and locking rows. SQL Server has a maximum nested trigger level and an option to disable recursive triggers; other DBMSs have engine-specific recursion settings. The real fix is to design trigger logic so it does not re-enter the same table, for example by using an INSTEAD OF trigger or a guard column.

**Why are triggers considered risky in high-throughput write paths?**

They add procedural work to every write inside the same transaction, can acquire locks in the trigger body, and make data changes depend on hidden code. A trigger that performs heavy queries or updates other tables serializes writes and complicates rollback analysis. Strong candidates explain that triggers are best reserved for invariants or side effects that cannot be expressed declaratively, and should be benchmarked under realistic write load.

## Worked example

Consider a SQL Server table Employees(EmployeeID, Name, Salary). A statement-level AFTER UPDATE trigger audits salary changes. An application runs UPDATE Employees SET Salary = Salary * 1.10 WHERE DepartmentID = 3, affecting two rows with old salaries 100000 and 80000. Because the trigger fires once for the whole statement, inserted holds both new salaries 110000 and 88000, while deleted holds both old salaries. The trigger body inserts into SalaryAudit by joining deleted and inserted on EmployeeID and filtering d.Salary <> i.Salary, producing two audit rows. Had the trigger body raised an error, the entire update would roll back because the trigger runs in the same transaction as the statement.

## Common traps

- Claiming AFTER triggers always fire after constraint checks: in PostgreSQL row-level AFTER triggers can run before deferred constraints, and deferrability changes when constraints are enforced.
- Writing a SQL Server trigger under the assumption it fires once per row, when DML triggers there are statement-level and inserted or deleted may contain many rows.
- Updating the same table inside an AFTER UPDATE trigger without a recursion guard, causing re-entry or hitting the engine's nested trigger limit.
- Forgetting that triggers execute inside the triggering transaction, so errors roll back both the trigger's work and the original DML statement.

</details>

---

### 59. Indexes · Easy

*sql · gate confidence 0.8*

<sub>to object to this card: `## sql-indexes` then `match: You are reviewing a database schema for an orders table. The`</sub>

**Question**

You are reviewing a database schema for an orders table. The team added the following index to speed up a query that filters by customer_id and order_date:

```sql
CREATE INDEX idx_orders_customer_date
ON orders (customer_id, order_date);
```

Later, a new query filters only by order_date:

```sql
SELECT * FROM orders WHERE order_date = '2024-05-01';
```

Which line in the index definition is the bug that prevents this new query from using the index efficiently?

**Options**

A. CREATE INDEX idx_orders_customer_date
B. ON orders (customer_id, order_date);

**Answer (the reader is graded on)**

- Correct: B. ON orders (customer_id, order_date);

**Reference answer**

The bug is the column order in the index definition: `customer_id` is the leading column, so the B-tree is sorted primarily by `customer_id`. A query filtering only on `order_date` cannot seek directly to the matching rows because `order_date` values are scattered across the index. The index cannot be used efficiently for this query.

**Graded on**

- A composite index can only be used efficiently for lookups that include leading columns.
- A query filtering only on a non-leading column cannot use the index for a seek.
- To support the new query, the index should have `order_date` as the leading column, or a separate index on `order_date` should be created.

<details><summary>The lesson this came from</summary>

An index is a separate data structure, usually a B-tree, that stores a sorted copy of one or more columns from a database table plus a pointer to the row the values came from. It lets the query planner seek or range-scan on key columns instead of scanning the entire table. Engines differ in clustering: SQL Server has one clustered index that determines physical row order and non-clustered indexes as separate B-trees; MySQL InnoDB always clusters by the primary key; PostgreSQL stores table rows in an unordered heap and all standard indexes are secondary.

## Why interviewers ask this

Interviewers use indexes to test whether you understand real database performance, not just syntax. They want to see you can choose a good index for a given query, reason about composite key order and covering indexes, and explain the write/storage tradeoff. Many candidates can recite CREATE INDEX but cannot predict when an index helps or hurts.

## The core idea

An index is a copy of data organized for search: it speeds up reads because the engine can walk a B-tree instead of scanning every row, but it adds storage and every insert/update/delete must keep the copies in sync. Composite indexes work left-to-right: equality columns position the seek, a range column bounds the scan, and later columns cannot narrow the seek range but can still be applied as predicates inside the index scan before row lookups in engines that support index condition pushdown. Write cost is engine-dependent: in PostgreSQL's append-only MVCC, an UPDATE creates a new tuple version and unless HOT optimization applies, all secondary indexes on the table receive entries for the new version, even when no indexed column changed.

## Key points

- Most general-purpose SQL indexes are B-trees that support O(log n + rows returned) seeks and range scans, compared with O(n) full table scans.
- A composite index on (a, b, c) can only be used efficiently for lookups that include leading columns; a query filtering only on b or c usually cannot use that index for a seek.
- For a WHERE clause with equality on a and range on b, c cannot narrow the seek range, but engines such as MySQL, SQL Server, PostgreSQL and Oracle can still apply c as an index filter while scanning the index.
- In SQL Server, clustered indexes define physical row order and are limited to one per table; MySQL InnoDB always has a clustered primary key; PostgreSQL has no clustered indexes and stores rows in a heap with secondary indexes pointing to row locations.
- In PostgreSQL's MVCC, an UPDATE writes a new tuple version and, unless HOT is possible on the same page, all secondary indexes are updated to point to the new version even if the updated columns are not part of any index.

## Your 60-second answer

A database index is a separate data structure, typically a B-tree, that keeps a sorted copy of one or more columns and pointers to the corresponding rows. It lets the optimizer find rows by seeking or scanning a small range instead of reading the whole table. In exchange, indexes consume storage and write operations must keep them in sync, so write-heavy tables can slow down significantly. How the columns are ordered matters: for a composite index, equality columns must come before range columns, and any column after the range cannot narrow the seek but can still be applied as a filter during the index scan in modern engines. Clustered indexes, where supported, define the table's physical order; non-clustered indexes are separate structures.

## If they dig deeper

**What are the main costs of creating too many indexes?**

Each index duplicates the key columns and adds storage. Writes must update indexes, increasing insert/update/delete latency. In MVCC engines like PostgreSQL, even updating a non-indexed column can force writes to every secondary index unless HOT optimization is possible on the same page.

**Given an index on (a, b, c) and WHERE a = 1 AND b > 2 AND c = 3, how much of the index is used?**

The B-tree can use a as an equality seek and then range scan b > 2. C cannot narrow the start or end of that b range because the index is sorted first by a, then b, so c values are not consecutive for all b > 2. Modern engines such as MySQL, SQL Server, PostgreSQL and Oracle still apply c as a residual predicate inside the index scan, avoiding base table lookups for rows that fail c = 3.

**Explain the difference between clustered and non-clustered indexes.**

A clustered index determines the physical order of table rows; SQL Server allows at most one per table and the leaf level is the data pages. MySQL InnoDB always stores rows in the primary key's clustered B-tree, with secondary indexes holding primary key values to find rows. PostgreSQL has no clustered index concept in its normal storage: rows live in an unordered heap, and every index, including the primary key, is a secondary structure pointing to row locations.

**Why does PostgreSQL update every secondary index when you change a non-indexed column?**

PostgreSQL uses MVCC: an UPDATE does not overwrite the old row, it writes a new physical tuple version. Every secondary index entry points to the physical tuple location, so the database must add entries for the new version into all indexes on the table. The HOT optimization avoids this only when the new tuple fits on the same heap page and no indexed column changes; then old index entries can be redirected via the line pointer, so secondary indexes remain unchanged.

## Worked example

Take an orders table with columns customer_id, order_date, status, and amount, and an index on (customer_id, order_date, status). A query asks: SELECT * FROM orders WHERE customer_id = 42 AND order_date BETWEEN '2024-01-01' AND '2024-06-30' AND status = 'shipped'. The B-tree descends to customer_id 42, then scans the order_date range as a contiguous block. Because the next key column status comes after order_date, it cannot start the scan at the first 'shipped' row inside that range; the scan visits all rows with order_date in that range. With index condition pushdown, the engine evaluates status = 'shipped' on the index entries and only performs base table lookups for rows that pass, avoiding I/O for rows that do not match. Without ICP, every row in the order_date range would trigger a lookup to check status.

## Common traps

- Believing an index on (a,b,c) can speed up a query that filters only on b or c; without leading column a, the B-tree cannot provide a direct seek.
- Over-indexing because each index helps a read; on a write-heavy table, the accumulated index maintenance can dominate and even hurt overall workload.
- Assuming 'c' is useless after a range on 'b' in a composite index; it cannot narrow the seek range but can still be used as an index filter before table access.
- Confusing clustered with unique: a clustered index concerns physical storage order, while a unique index is a constraint that rejects duplicate key values.

</details>

---

## Tap the bottleneck (`tap-the-bottleneck` · tap_in_place)

### 60. Publish-subscribe · Easy

*system_design · gate confidence 0.75*

<sub>to object to this card: `## sd-publish-subscribe` then `match: A system uses Redis Pub/Sub to deliver chat messages to onli`</sub>

**Question**

A system uses Redis Pub/Sub to deliver chat messages to online users. Which line is the bottleneck that causes offline users to permanently miss messages?

**Options**

A. 1. Publisher sends message to topic 'chat'
B. 2. Broker fans out to all current subscribers
C. 3. Subscriber not connected at publish time
D. 4. Subscriber reconnects and requests missed messages

**Answer (the reader is graded on)**

- Correct: C. 3. Subscriber not connected at publish time

**Reference answer**

Line 3 is the bottleneck: Redis Pub/Sub is in-memory only and does not persist messages, so any subscriber not connected at publish time loses the message permanently.

**Graded on**

- Redis Pub/Sub provides no persistence or replay.
- Offline subscribers miss messages published while disconnected.
- Durable storage is required for offline delivery.

<details><summary>The lesson this came from</summary>

Publish-subscribe is a messaging pattern where publishers send messages to a named topic and a broker delivers each message to every current subscriber of that topic. The publisher does not address specific consumers, and subscribers do not need to know which producer sent a message. This creates one-to-many fan-out with independent, parallel consumption. Delivery semantics vary by broker: Redis Pub/Sub is in-memory only with no persistence or replay, while Kafka stores messages in a durable log and supports replay from offsets.

## Why interviewers ask this

Interviewers use Messenger, Instagram, and Twitter designs to test whether you can decouple producers from consumers and scale fan-out to millions of users. They are probing your understanding of delivery guarantees, offline handling, protocol choice, and the fan-out-on-write versus fan-out-on-read trade-off. A strong answer shows you know when pub/sub alone is insufficient and where durable storage or hybrid fan-out is required.

## The core idea

The essence is decoupling: the broker holds subscriptions and routes each published message to all interested subscribers, so adding a subscriber or scaling consumers does not change the publisher. This enables parallel processing and independent scaling, but it moves the reliability burden to the broker and consumers. Delivery is best understood as a spectrum from transient fire-and-forget (Redis Pub/Sub) to durable, replayable logs (Kafka). In feed and chat systems, the central design choice is whether to write the message into every recipient's inbox at publish time (fan-out on write) or compute each recipient's view at read time (fan-out on read), often hybridized by follower count.

## Key points

- Pub-sub decouples publishers from subscribers through a broker and a named topic, enabling one-to-many fan-out without the publisher knowing recipient identities.
- Redis Pub/Sub is strictly in-memory and transient: it provides no persistence, durability, or message replay under any configuration, so messages published while a subscriber is offline are lost.
- Kafka persists messages in a durable, partitioned log and lets consumers replay from committed offsets, so it can serve as a durable pub/sub substrate but is not a drop-in replacement for Redis Pub/Sub.
- Fan-out on write inserts the message into each recipient's inbox at publish time, minimizing read latency at the cost of write amplification; fan-out on read computes the feed from a central timeline, avoiding write amplification but increasing read cost.
- Pure publish-subscribe does not guarantee exactly-once end-to-end delivery; achieving an exactly-once effect requires persistent storage, acknowledgments, retries, deduplication, and idempotent consumers.

## Your 60-second answer

Publish-subscribe is a messaging pattern where publishers send events to a topic, and a broker fans each event out to all subscribers of that topic, without the publisher knowing who receives it. The broker decouples producers from consumers and allows subscribers to scale and process messages independently. The main trade-off is delivery semantics. A transient broker like Redis Pub/Sub keeps no messages on disk, so any subscriber not connected at publish time loses that message permanently. A durable log like Kafka stores messages and lets consumers replay from offsets, but it shifts the API and operational model. For a chat or feed design, I would not rely on pub/sub alone: I'd persist messages in per-user inboxes, push via WebSockets to connected devices, and let offline devices pull missing messages by sequence ID. For celebrities, I'd avoid writing to millions of inboxes and use fan-out on read or a hybrid threshold.

## If they dig deeper

**How do you ensure low-latency message delivery (<100ms) across millions of users?**

Keep persistent WebSocket connections to regional gateway servers, and have those gateways subscribe to user topics on an in-memory broker. Publish to the broker and fan out to only the connection servers holding active sessions, with backpressure and batching; avoid writing to disk on the hot path. Track p95 and p99 latency per region and shed load or degrade to pull-based delivery if the fan-out cannot meet the target.

**What communication protocol will you use: long polling, WebSockets?**

Use WebSockets for bidirectional, low-overhead real-time delivery because the server can push a message immediately. Fall back to long polling where proxies or clients block WebSockets, but long polling adds per-request overhead and latency. HTTP/2 server push is not a reliable replacement because it is tied to a single request-response stream.

**How do you handle offline users and guarantee eventual delivery?**

Persist the message in a durable per-user inbox or outbox before acknowledging the publish, so it is not lost if the subscriber is offline. When a device reconnects, it sends its last seen message ID or timestamp and pulls all missing messages in order. Use idempotent writes and a notification service for mobile devices to wake the app, since WebSockets are not alive in background.

**How do you support multi-device sync so message states are consistent across devices?**

Keep a single source of truth for each user's inbox on the server, with per-device cursors tracking the last message ID each device has seen. Device actions like read receipts update the server state, and the server fans out state changes to other devices via the same pub/sub topic. Reconcile offline edits by last-write-wins or a version vector if concurrent updates need to merge.

**How will you manage group messaging: fan-out on write vs fan-out on read?**

For small groups, fan out on write by inserting the message into each member's inbox, giving low read latency with manageable write amplification. For very large groups or channels, store one copy in a group timeline and let members read it with a cursor, avoiding millions of writes per message. Many systems use a hybrid threshold: fan out on write below a few thousand members and switch to fan-out on read above that, possibly with backfill for active members.

## Worked example

Consider a group chat with 1,000 members. A message service receives a message 'hello' from user A for group G. With fan-out on write, it first writes the message to a messages table with message_id 5001, group_id G, sender A, and timestamp 1700000000, then inserts 1,000 envelope rows into member_inbox(user_id, message_id, received_at). A connected member's device receives the push via its WebSocket gateway; an offline member gets the row persisted and pulls it later by querying member_inbox where user_id = ? and message_id > last_seen. For a 10,000,000-member channel, the same approach would create 10,000,000 envelope rows per message, causing write amplification and storage cost. Fan-out on read stores only the one message and lets members query messages where group_id = G and timestamp > cursor, with an index on (group_id, timestamp); read latency is higher but write cost is constant. A hybrid system can fan out on write for groups under 1,000 members and fan out on read for larger groups.

## Common traps

- Treating Redis Pub/Sub as a durable queue: it discards any message not received by a connected subscriber and has no replay or persistence, regardless of Redis configuration.
- Claiming pub/sub gives exactly-once delivery: without persistent logs, acknowledgments, and idempotent consumers, messages can be lost or duplicated.
- Applying fan-out on write uniformly to accounts with millions of followers (celebrities), which causes write amplification so large it can overwhelm the database and delay publish.
- Ignoring broker failure as a single point of failure and not planning for subscriber reconnection, causing missed messages and stale subscriptions after partitions.

</details>

---

### 61. Triggers · Medium

*sql · gate confidence 0.8*

<sub>to object to this card: `## sql-triggers` then `match: A SQL Server AFTER UPDATE trigger on the Employees table is `</sub>

**Question**

A SQL Server AFTER UPDATE trigger on the Employees table is intended to audit salary changes. The trigger body is shown below. Which line is the bottleneck that causes the trigger to fire recursively and eventually hit the nested trigger limit?

1  CREATE TRIGGER trg_AuditSalary
2  ON Employees
3  AFTER UPDATE
4  AS
5  BEGIN
6      INSERT INTO SalaryAudit (EmployeeID, OldSalary, NewSalary)
7      SELECT d.EmployeeID, d.Salary, i.Salary
8      FROM deleted d
9      INNER JOIN inserted i ON d.EmployeeID = i.EmployeeID
10     WHERE d.Salary <> i.Salary;
11 END;

**Options**

A. CREATE TRIGGER trg_AuditSalary
B. ON Employees
C. AFTER UPDATE
D. AS
E. BEGIN
F. INSERT INTO SalaryAudit (EmployeeID, OldSalary, NewSalary)
G. SELECT d.EmployeeID, d.Salary, i.Salary
H. FROM deleted d
I. INNER JOIN inserted i ON d.EmployeeID = i.EmployeeID
J. WHERE d.Salary <> i.Salary;
K. END;

**Answer (the reader is graded on)**

- Correct: C. AFTER UPDATE

**Reference answer**

Line 3 is the bottleneck. The AFTER UPDATE trigger fires after the UPDATE statement on Employees, and the trigger body itself does not modify Employees, so it does not cause recursion. However, if the trigger body were to update Employees, it would fire recursively. In this specific trigger, there is no recursive update, so the bottleneck is the AFTER UPDATE timing itself, which is the only line that could lead to recursion if the trigger body were changed to update the same table.

**Graded on**

- AFTER UPDATE triggers fire after the triggering UPDATE statement.
- The trigger body shown does not update Employees, so it does not cause recursion.
- Recursion occurs only if the trigger body performs DML on the same table.
- SQL Server has a nested trigger limit that can be hit by recursive triggers.

<details><summary>The lesson this came from</summary>

A trigger is a database object bound to a table or view that automatically executes procedural SQL in response to specified DML (INSERT, UPDATE, DELETE) or DDL events. SQL Server implements DML triggers as statement-level procedures with inserted and deleted pseudo-tables; PostgreSQL supports row-level and statement-level triggers with OLD and NEW record values; MySQL implements row-level BEFORE and AFTER triggers on tables. The trigger body runs in the same transaction as the triggering statement unless the DBMS provides separate autonomous transaction features.

## Why interviewers ask this

Interviewers ask about triggers to see whether you understand how database-enforced logic differs from application logic: it runs automatically, cannot be bypassed by a client, and can hide side effects inside write paths. They probe transaction and timing semantics because a candidate who thinks all DBMSs fire AFTER triggers after constraint checks will make costly schema or recovery mistakes.

## The core idea

A trigger is a stored routine tied to an event rather than called by a client. DML changes construct transition data: SQL Server exposes inserted and deleted pseudo-tables containing the full set of affected rows for one statement; PostgreSQL and MySQL row-level triggers expose OLD and NEW values per row. The trigger executes in the same transaction as the DML, so its effects either commit or roll back with the statement unless the DBMS has autonomous transaction support. Because trigger timing relative to constraint checking differs by engine—SQL Server AFTER is post-constraint, while PostgreSQL row-level AFTER can run before deferred constraints—you must state the DBMS when discussing ordering. Recursive or long-running triggers are a common source of surprising locks and rollbacks.

## Key points

- SQL Server DML triggers are statement-level and fire once per INSERT, UPDATE, or DELETE statement, using inserted and deleted pseudo-tables for new and old row sets.
- PostgreSQL supports row-level and statement-level BEFORE, AFTER, and on views INSTEAD OF triggers; MySQL supports only row-level BEFORE and AFTER triggers on tables.
- SQL Server AFTER triggers run after the triggering DML and after constraint checks, but in PostgreSQL row-level AFTER triggers run before deferred constraint checks, and constraint timing depends on deferrability.
- In SQL Server, INSTEAD OF triggers can be defined on tables or views, while AFTER/FOR triggers cannot be defined on views.
- A trigger executes in the same transaction as the triggering statement, so an error in the trigger normally rolls back the statement, and recursive triggers can hit engine-defined nesting limits.

## Your 60-second answer

A trigger is a database object that automatically executes procedural code when a specified DML or DDL event occurs on a table or view. In SQL Server I can define an AFTER UPDATE trigger to audit salary changes; it fires once per statement and reads the inserted and deleted pseudo-tables, which hold the new and old row sets. PostgreSQL and MySQL use OLD and NEW record references in row-level triggers instead. The main benefit is enforcing logic inside the storage layer so no client can bypass it; the trade-off is that the trigger runs in the same transaction, can hide side effects, slow writes, and cause recursive cascades. I also qualify timing: SQL Server AFTER runs after constraint checks, but PostgreSQL row-level AFTER can run before deferred constraints. I use triggers only for cross-row invariants, auditing, or denormalization that constraints cannot express.

## If they dig deeper

**In SQL Server, what are the inserted and deleted tables inside a trigger?**

They are pseudo-tables available only inside DML triggers. INSERT and UPDATE populate inserted with new values; DELETE and UPDATE populate deleted with old values. Because SQL Server DML triggers fire once per statement, these pseudo-tables contain all rows affected by that statement, and you join them on the primary key to compare old and new values.

**What is the difference between AFTER and INSTEAD OF triggers in SQL Server?**

AFTER triggers execute after the DML operation has been applied and, in SQL Server, after constraints have been checked; they cannot be defined on views. INSTEAD OF triggers replace the DML operation entirely, run before any changes are made, and can be defined on tables or views, which is how views are made updatable in SQL Server.

**How do BEFORE and AFTER row-level triggers compare in PostgreSQL, and when does constraint checking happen?**

In PostgreSQL, a BEFORE row-level trigger fires before the row is written and can modify the NEW record, while an AFTER row-level trigger fires after the row is written but before the end of the statement. Non-deferred constraints are checked immediately or at statement end depending on type; deferred constraints are checked at commit. Thus a row-level AFTER trigger can see changes before a deferred constraint check rejects them.

**What problems do recursive triggers cause and how are they controlled?**

A trigger that performs the same DML on its own table can fire itself repeatedly, consuming resources and locking rows. SQL Server has a maximum nested trigger level and an option to disable recursive triggers; other DBMSs have engine-specific recursion settings. The real fix is to design trigger logic so it does not re-enter the same table, for example by using an INSTEAD OF trigger or a guard column.

**Why are triggers considered risky in high-throughput write paths?**

They add procedural work to every write inside the same transaction, can acquire locks in the trigger body, and make data changes depend on hidden code. A trigger that performs heavy queries or updates other tables serializes writes and complicates rollback analysis. Strong candidates explain that triggers are best reserved for invariants or side effects that cannot be expressed declaratively, and should be benchmarked under realistic write load.

## Worked example

Consider a SQL Server table Employees(EmployeeID, Name, Salary). A statement-level AFTER UPDATE trigger audits salary changes. An application runs UPDATE Employees SET Salary = Salary * 1.10 WHERE DepartmentID = 3, affecting two rows with old salaries 100000 and 80000. Because the trigger fires once for the whole statement, inserted holds both new salaries 110000 and 88000, while deleted holds both old salaries. The trigger body inserts into SalaryAudit by joining deleted and inserted on EmployeeID and filtering d.Salary <> i.Salary, producing two audit rows. Had the trigger body raised an error, the entire update would roll back because the trigger runs in the same transaction as the statement.

## Common traps

- Claiming AFTER triggers always fire after constraint checks: in PostgreSQL row-level AFTER triggers can run before deferred constraints, and deferrability changes when constraints are enforced.
- Writing a SQL Server trigger under the assumption it fires once per row, when DML triggers there are statement-level and inserted or deleted may contain many rows.
- Updating the same table inside an AFTER UPDATE trigger without a recursion guard, causing re-entry or hitting the engine's nested trigger limit.
- Forgetting that triggers execute inside the triggering transaction, so errors roll back both the trigger's work and the original DML statement.

</details>

---

## Tap the insertion point (`tap-the-insertion-point` · tap_in_place)

### 62. Indexes · Medium

*sql · gate confidence 0.8*

<sub>to object to this card: `## sql-indexes` then `match: You are reviewing a table definition and a query for a Postg`</sub>

**Question**

You are reviewing a table definition and a query for a PostgreSQL database. Which line contains the bottleneck that an index could fix?

```sql
1  CREATE TABLE orders (
2      id SERIAL PRIMARY KEY,
3      customer_id INT NOT NULL,
4      order_date DATE NOT NULL,
5      status TEXT NOT NULL,
6      amount NUMERIC(10,2) NOT NULL
7  );
8
9  SELECT *
10 FROM orders
11 WHERE customer_id = 42
12   AND order_date BETWEEN '2024-01-01' AND '2024-06-30'
13   AND status = 'shipped';
```

**Options**

A. 1  CREATE TABLE orders (
B. 2      id SERIAL PRIMARY KEY,
C. 3      customer_id INT NOT NULL,
D. 4      order_date DATE NOT NULL,
E. 5      status TEXT NOT NULL,
F. 6      amount NUMERIC(10,2) NOT NULL
G. 7  );
H. 8
I. 9  SELECT *
J. 10 FROM orders
K. 11 WHERE customer_id = 42
L. 12   AND order_date BETWEEN '2024-01-01' AND '2024-06-30'
M. 13   AND status = 'shipped';

**Answer (the reader is graded on)**

- Correct: K. 11 WHERE customer_id = 42

**Reference answer**

Line 11 is the bottleneck: the query filters on customer_id, but there is no index on that column, so PostgreSQL must perform a full table scan. An index on (customer_id, order_date) would let the engine seek directly to customer_id 42 and range-scan the order_date values.

**Graded on**

- Without an index on customer_id, the query cannot seek and must scan the entire table.
- A composite index on (customer_id, order_date) supports both the equality on customer_id and the range on order_date.
- The status predicate can be applied as a filter during the index scan, but it cannot narrow the seek range.

<details><summary>The lesson this came from</summary>

An index is a separate data structure, usually a B-tree, that stores a sorted copy of one or more columns from a database table plus a pointer to the row the values came from. It lets the query planner seek or range-scan on key columns instead of scanning the entire table. Engines differ in clustering: SQL Server has one clustered index that determines physical row order and non-clustered indexes as separate B-trees; MySQL InnoDB always clusters by the primary key; PostgreSQL stores table rows in an unordered heap and all standard indexes are secondary.

## Why interviewers ask this

Interviewers use indexes to test whether you understand real database performance, not just syntax. They want to see you can choose a good index for a given query, reason about composite key order and covering indexes, and explain the write/storage tradeoff. Many candidates can recite CREATE INDEX but cannot predict when an index helps or hurts.

## The core idea

An index is a copy of data organized for search: it speeds up reads because the engine can walk a B-tree instead of scanning every row, but it adds storage and every insert/update/delete must keep the copies in sync. Composite indexes work left-to-right: equality columns position the seek, a range column bounds the scan, and later columns cannot narrow the seek range but can still be applied as predicates inside the index scan before row lookups in engines that support index condition pushdown. Write cost is engine-dependent: in PostgreSQL's append-only MVCC, an UPDATE creates a new tuple version and unless HOT optimization applies, all secondary indexes on the table receive entries for the new version, even when no indexed column changed.

## Key points

- Most general-purpose SQL indexes are B-trees that support O(log n + rows returned) seeks and range scans, compared with O(n) full table scans.
- A composite index on (a, b, c) can only be used efficiently for lookups that include leading columns; a query filtering only on b or c usually cannot use that index for a seek.
- For a WHERE clause with equality on a and range on b, c cannot narrow the seek range, but engines such as MySQL, SQL Server, PostgreSQL and Oracle can still apply c as an index filter while scanning the index.
- In SQL Server, clustered indexes define physical row order and are limited to one per table; MySQL InnoDB always has a clustered primary key; PostgreSQL has no clustered indexes and stores rows in a heap with secondary indexes pointing to row locations.
- In PostgreSQL's MVCC, an UPDATE writes a new tuple version and, unless HOT is possible on the same page, all secondary indexes are updated to point to the new version even if the updated columns are not part of any index.

## Your 60-second answer

A database index is a separate data structure, typically a B-tree, that keeps a sorted copy of one or more columns and pointers to the corresponding rows. It lets the optimizer find rows by seeking or scanning a small range instead of reading the whole table. In exchange, indexes consume storage and write operations must keep them in sync, so write-heavy tables can slow down significantly. How the columns are ordered matters: for a composite index, equality columns must come before range columns, and any column after the range cannot narrow the seek but can still be applied as a filter during the index scan in modern engines. Clustered indexes, where supported, define the table's physical order; non-clustered indexes are separate structures.

## If they dig deeper

**What are the main costs of creating too many indexes?**

Each index duplicates the key columns and adds storage. Writes must update indexes, increasing insert/update/delete latency. In MVCC engines like PostgreSQL, even updating a non-indexed column can force writes to every secondary index unless HOT optimization is possible on the same page.

**Given an index on (a, b, c) and WHERE a = 1 AND b > 2 AND c = 3, how much of the index is used?**

The B-tree can use a as an equality seek and then range scan b > 2. C cannot narrow the start or end of that b range because the index is sorted first by a, then b, so c values are not consecutive for all b > 2. Modern engines such as MySQL, SQL Server, PostgreSQL and Oracle still apply c as a residual predicate inside the index scan, avoiding base table lookups for rows that fail c = 3.

**Explain the difference between clustered and non-clustered indexes.**

A clustered index determines the physical order of table rows; SQL Server allows at most one per table and the leaf level is the data pages. MySQL InnoDB always stores rows in the primary key's clustered B-tree, with secondary indexes holding primary key values to find rows. PostgreSQL has no clustered index concept in its normal storage: rows live in an unordered heap, and every index, including the primary key, is a secondary structure pointing to row locations.

**Why does PostgreSQL update every secondary index when you change a non-indexed column?**

PostgreSQL uses MVCC: an UPDATE does not overwrite the old row, it writes a new physical tuple version. Every secondary index entry points to the physical tuple location, so the database must add entries for the new version into all indexes on the table. The HOT optimization avoids this only when the new tuple fits on the same heap page and no indexed column changes; then old index entries can be redirected via the line pointer, so secondary indexes remain unchanged.

## Worked example

Take an orders table with columns customer_id, order_date, status, and amount, and an index on (customer_id, order_date, status). A query asks: SELECT * FROM orders WHERE customer_id = 42 AND order_date BETWEEN '2024-01-01' AND '2024-06-30' AND status = 'shipped'. The B-tree descends to customer_id 42, then scans the order_date range as a contiguous block. Because the next key column status comes after order_date, it cannot start the scan at the first 'shipped' row inside that range; the scan visits all rows with order_date in that range. With index condition pushdown, the engine evaluates status = 'shipped' on the index entries and only performs base table lookups for rows that pass, avoiding I/O for rows that do not match. Without ICP, every row in the order_date range would trigger a lookup to check status.

## Common traps

- Believing an index on (a,b,c) can speed up a query that filters only on b or c; without leading column a, the B-tree cannot provide a direct seek.
- Over-indexing because each index helps a read; on a write-heavy table, the accumulated index maintenance can dominate and even hurt overall workload.
- Assuming 'c' is useless after a range on 'b' in a composite index; it cannot narrow the seek range but can still be used as an index filter before table access.
- Confusing clustered with unique: a clustered index concerns physical storage order, while a unique index is a constraint that rejects duplicate key values.

</details>

---

### 63. Indexes · Medium

*sql · gate confidence 0.8*

<sub>to object to this card: `## sql-indexes` then `match: You are reviewing a table definition and a query for an e-co`</sub>

**Question**

You are reviewing a table definition and a query for an e-commerce database. The table has a composite index on (customer_id, order_date, status).

```sql
CREATE INDEX idx_orders_customer_date_status
ON orders (customer_id, order_date, status);

SELECT *
FROM orders
WHERE customer_id = 42
  AND order_date BETWEEN '2024-01-01' AND '2024-06-30'
  AND status = 'shipped';
```

Which line in the query prevents the database from using the index to directly seek to the rows with status = 'shipped'?

**Options**

A. SELECT *
B. FROM orders
C. WHERE customer_id = 42
D. AND order_date BETWEEN '2024-01-01' AND '2024-06-30'
E. AND status = 'shipped'

**Answer (the reader is graded on)**

- Correct: D. AND order_date BETWEEN '2024-01-01' AND '2024-06-30'

**Reference answer**

The line `AND order_date BETWEEN '2024-01-01' AND '2024-06-30'` is the range condition on the second column of the composite index. Because the index is sorted by (customer_id, order_date, status), once the scan is bounded by the order_date range, the status values are not contiguous within that range, so the database cannot seek directly to rows with status = 'shipped'. It must scan all index entries in the order_date range and apply status as a filter.

**Graded on**

- A composite index is sorted by its columns in order, so a range on an earlier column prevents a seek on later columns.
- The status condition can still be applied as a filter during the index scan, but it does not narrow the seek range.
- The equality on customer_id is used to position the seek, and the range on order_date bounds the scan.

<details><summary>The lesson this came from</summary>

An index is a separate data structure, usually a B-tree, that stores a sorted copy of one or more columns from a database table plus a pointer to the row the values came from. It lets the query planner seek or range-scan on key columns instead of scanning the entire table. Engines differ in clustering: SQL Server has one clustered index that determines physical row order and non-clustered indexes as separate B-trees; MySQL InnoDB always clusters by the primary key; PostgreSQL stores table rows in an unordered heap and all standard indexes are secondary.

## Why interviewers ask this

Interviewers use indexes to test whether you understand real database performance, not just syntax. They want to see you can choose a good index for a given query, reason about composite key order and covering indexes, and explain the write/storage tradeoff. Many candidates can recite CREATE INDEX but cannot predict when an index helps or hurts.

## The core idea

An index is a copy of data organized for search: it speeds up reads because the engine can walk a B-tree instead of scanning every row, but it adds storage and every insert/update/delete must keep the copies in sync. Composite indexes work left-to-right: equality columns position the seek, a range column bounds the scan, and later columns cannot narrow the seek range but can still be applied as predicates inside the index scan before row lookups in engines that support index condition pushdown. Write cost is engine-dependent: in PostgreSQL's append-only MVCC, an UPDATE creates a new tuple version and unless HOT optimization applies, all secondary indexes on the table receive entries for the new version, even when no indexed column changed.

## Key points

- Most general-purpose SQL indexes are B-trees that support O(log n + rows returned) seeks and range scans, compared with O(n) full table scans.
- A composite index on (a, b, c) can only be used efficiently for lookups that include leading columns; a query filtering only on b or c usually cannot use that index for a seek.
- For a WHERE clause with equality on a and range on b, c cannot narrow the seek range, but engines such as MySQL, SQL Server, PostgreSQL and Oracle can still apply c as an index filter while scanning the index.
- In SQL Server, clustered indexes define physical row order and are limited to one per table; MySQL InnoDB always has a clustered primary key; PostgreSQL has no clustered indexes and stores rows in a heap with secondary indexes pointing to row locations.
- In PostgreSQL's MVCC, an UPDATE writes a new tuple version and, unless HOT is possible on the same page, all secondary indexes are updated to point to the new version even if the updated columns are not part of any index.

## Your 60-second answer

A database index is a separate data structure, typically a B-tree, that keeps a sorted copy of one or more columns and pointers to the corresponding rows. It lets the optimizer find rows by seeking or scanning a small range instead of reading the whole table. In exchange, indexes consume storage and write operations must keep them in sync, so write-heavy tables can slow down significantly. How the columns are ordered matters: for a composite index, equality columns must come before range columns, and any column after the range cannot narrow the seek but can still be applied as a filter during the index scan in modern engines. Clustered indexes, where supported, define the table's physical order; non-clustered indexes are separate structures.

## If they dig deeper

**What are the main costs of creating too many indexes?**

Each index duplicates the key columns and adds storage. Writes must update indexes, increasing insert/update/delete latency. In MVCC engines like PostgreSQL, even updating a non-indexed column can force writes to every secondary index unless HOT optimization is possible on the same page.

**Given an index on (a, b, c) and WHERE a = 1 AND b > 2 AND c = 3, how much of the index is used?**

The B-tree can use a as an equality seek and then range scan b > 2. C cannot narrow the start or end of that b range because the index is sorted first by a, then b, so c values are not consecutive for all b > 2. Modern engines such as MySQL, SQL Server, PostgreSQL and Oracle still apply c as a residual predicate inside the index scan, avoiding base table lookups for rows that fail c = 3.

**Explain the difference between clustered and non-clustered indexes.**

A clustered index determines the physical order of table rows; SQL Server allows at most one per table and the leaf level is the data pages. MySQL InnoDB always stores rows in the primary key's clustered B-tree, with secondary indexes holding primary key values to find rows. PostgreSQL has no clustered index concept in its normal storage: rows live in an unordered heap, and every index, including the primary key, is a secondary structure pointing to row locations.

**Why does PostgreSQL update every secondary index when you change a non-indexed column?**

PostgreSQL uses MVCC: an UPDATE does not overwrite the old row, it writes a new physical tuple version. Every secondary index entry points to the physical tuple location, so the database must add entries for the new version into all indexes on the table. The HOT optimization avoids this only when the new tuple fits on the same heap page and no indexed column changes; then old index entries can be redirected via the line pointer, so secondary indexes remain unchanged.

## Worked example

Take an orders table with columns customer_id, order_date, status, and amount, and an index on (customer_id, order_date, status). A query asks: SELECT * FROM orders WHERE customer_id = 42 AND order_date BETWEEN '2024-01-01' AND '2024-06-30' AND status = 'shipped'. The B-tree descends to customer_id 42, then scans the order_date range as a contiguous block. Because the next key column status comes after order_date, it cannot start the scan at the first 'shipped' row inside that range; the scan visits all rows with order_date in that range. With index condition pushdown, the engine evaluates status = 'shipped' on the index entries and only performs base table lookups for rows that pass, avoiding I/O for rows that do not match. Without ICP, every row in the order_date range would trigger a lookup to check status.

## Common traps

- Believing an index on (a,b,c) can speed up a query that filters only on b or c; without leading column a, the B-tree cannot provide a direct seek.
- Over-indexing because each index helps a read; on a write-heavy table, the accumulated index maintenance can dominate and even hurt overall workload.
- Assuming 'c' is useless after a range on 'b' in a composite index; it cannot narrow the seek range but can still be used as an index filter before table access.
- Confusing clustered with unique: a clustered index concerns physical storage order, while a unique index is a constraint that rejects duplicate key values.

</details>

---

## Tap the unsafe line (`tap-the-unsafe-line` · tap_in_place)

### 64. Load balancing · Medium

*system_design · gate confidence 0.7*

<sub>to object to this card: `## sd-load-balancing` then `match: A load balancer configuration is shown below. Which line is `</sub>

**Question**

A load balancer configuration is shown below. Which line is unsafe for a production system that must survive a load balancer failure?

1. upstream backend {
2.   server 10.0.0.1:80;
3.   server 10.0.0.2:80;
4. }
5. server {
6.   listen 80;
7.   location / {
8.     proxy_pass http://backend;
9.   }
10. }

**Options**

A. upstream backend {
B. server 10.0.0.1:80;
C. server 10.0.0.2:80;
D. }
E. server {
F. listen 80;
G. location / {
H. proxy_pass http://backend;
I. }
J. }

**Answer (the reader is graded on)**

- Correct: F. listen 80;

**Reference answer**

Line 6 is unsafe because the load balancer listens on a single IP address and port without any redundancy. If this load balancer instance fails, all traffic stops. A production setup needs at least two load balancers in an active-passive or active-active pair, typically sharing a virtual IP via VRRP or a cloud service.

**Graded on**

- A single load balancer is a single point of failure.
- High availability requires redundant load balancers with failover.
- The configuration shown has no mechanism for another instance to take over.

<details><summary>The lesson this came from</summary>

Load balancing distributes incoming network or application traffic across multiple backend servers using a configurable algorithm and health checks. It prevents a single server from becoming a bottleneck, improves throughput and response time, and enables horizontal scaling by adding or removing servers without changing clients. Load balancers can operate at Layer 4 (transport, TCP/UDP) or Layer 7 (application, HTTP).

## Why interviewers ask this

Interviewers use load balancing to test whether you can design for scale, availability, and failure handling. They expect you to choose an algorithm for the workload, explain where balancing happens in a multi-tier architecture, and describe how health checks and failover keep the system online.

## The core idea

A load balancer sits in front of a pool of servers and chooses which server receives each request based on an algorithm. It stops serving unhealthy instances and lets you add or remove capacity without disrupting clients. The algorithm matters less than correct health checking and the distinction between Layer 4 (connection-level) and Layer 7 (request/content-level) routing. For stateful workloads you may need session affinity; for uneven server capacity, weighted algorithms.

## Key points

- A health check marks backend instances as healthy or unhealthy; the load balancer routes only to healthy instances and can trigger failover.
- Round robin cycles sequentially and suits uniform, stateless servers; weighted round robin adds capacity weights.
- Least connections sends a new request to the server with the fewest active connections and adapts to uneven workloads.
- Layer 4 load balancers route using IP and TCP/UDP data, while Layer 7 load balancers inspect HTTP headers, cookies, or paths.
- High availability requires the load balancer itself to be redundant, often via active-passive pairs or multiple load balancers with DNS failover.

## Your 60-second answer

A load balancer sits in front of backend servers and distributes incoming requests across them. It avoids overloading one machine, keeps latency low, and lets the system tolerate server failures. The balancer uses periodic health checks to take unhealthy servers out of rotation, and an algorithm to select a target: round robin, least connections, or IP hash are common. Layer 4 balancers route on connection-level data, while Layer 7 balancers can inspect HTTP and route by path or cookie. The main trade-off is that the load balancer adds an extra hop and can become a single point of failure, so production systems deploy it in pairs or rely on managed cloud balancers.

## If they dig deeper

**What is the difference between Layer 4 and Layer 7 load balancing?**

Layer 4 balances using transport-layer data like IP addresses and TCP/UDP ports, without inspecting payload, so it is fast and works for any TCP/UDP protocol. Layer 7 terminates and inspects HTTP, enabling routing by URL path, headers, or cookies, and can also handle TLS termination, but uses more CPU.

**How do health checks work, and what happens when an instance fails?**

Active health checks periodically send TCP, HTTP, or gRPC probes to each backend; passive checks infer health from actual request outcomes. After a configured number of failures, the load balancer marks the instance unhealthy and removes it from rotation, so new requests go to healthy servers; it re-adds the instance once checks pass again.

**Which algorithm would you choose for a service with long-lived connections of varying duration?**

Least connections or least response time is better because round robin can accidentally pile many long-lived connections onto one server. A Layer 4 least-connections balancer works well for raw TCP; if content-based routing is needed, use a Layer 7 balancer with HTTP metrics.

**How do you maintain session state when users need to stay on the same server?**

You can use session affinity, or sticky sessions, via a cookie or IP hash so a user returns to the same backend. This hurts even distribution and failover, so the stronger approach is to keep sessions in a shared store such as Redis and let any server serve the request.

**How do you make the load balancer itself highly available?**

Deploy at least two load balancers in an active-passive or active-active pair, share a virtual IP using VRRP or a cloud service, and use health checks between the balancers so a standby takes over automatically. DNS can also point to multiple balancers, and anycast can route clients to the nearest healthy one.

## Worked example

Three servers sit behind a load balancer. With round robin and all healthy, requests 1 through 9 are assigned A, B, C, A, B, C, A, B, C. Now suppose each request holds its connection for a different length of time: A is handling 5 active requests, B 2, and C 0. A least-connections balancer sends the next request to C because it has the fewest current connections, even though round robin might have pointed to A. If C then fails, health checks mark it unhealthy after repeated failed probes and remove it from the pool, so traffic is distributed only across A and B until C passes checks again.

## Common traps

- Choosing an algorithm only for fairness without accounting for variable request duration or heterogeneous server capacity.
- Forgetting that the load balancer itself is a single point of failure unless deployed redundantly.
- Using IP-hash or sticky sessions as a substitute for shared session storage, which breaks failover and horizontal scaling.
- Ignoring health checks: a balancer that routes to a dead instance will still send user traffic and cause errors.

</details>

---

### 65. Publish-subscribe · Medium

*system_design · gate confidence 0.75*

<sub>to object to this card: `## sd-publish-subscribe` then `match: A system design candidate proposes the following architectur`</sub>

**Question**

A system design candidate proposes the following architecture for a real-time chat application. Which line is unsafe?

1. Publisher sends message to topic 'chat' on Redis Pub/Sub.
2. Redis Pub/Sub fans out the message to all connected subscribers.
3. Subscriber receives the message and displays it to the user.
4. If a subscriber is offline, the message is stored in a durable queue for later delivery.
5. When the subscriber reconnects, it reads the queued message and displays it.

**Options**

A. Publisher sends message to topic 'chat' on Redis Pub/Sub.
B. Redis Pub/Sub fans out the message to all connected subscribers.
C. Subscriber receives the message and displays it to the user.
D. If a subscriber is offline, the message is stored in a durable queue for later delivery.
E. When the subscriber reconnects, it reads the queued message and displays it.

**Answer (the reader is graded on)**

- Correct: D. If a subscriber is offline, the message is stored in a durable queue for later delivery.

**Reference answer**

Line 4 is unsafe because Redis Pub/Sub is strictly in-memory and transient; it does not store messages for offline subscribers. Any message published while a subscriber is offline is lost, so there is no durable queue to read from later.

**Graded on**

- Redis Pub/Sub provides no persistence or replay.
- Offline subscribers miss messages permanently.
- Durable delivery requires a persistent store like Kafka or a database.

<details><summary>The lesson this came from</summary>

Publish-subscribe is a messaging pattern where publishers send messages to a named topic and a broker delivers each message to every current subscriber of that topic. The publisher does not address specific consumers, and subscribers do not need to know which producer sent a message. This creates one-to-many fan-out with independent, parallel consumption. Delivery semantics vary by broker: Redis Pub/Sub is in-memory only with no persistence or replay, while Kafka stores messages in a durable log and supports replay from offsets.

## Why interviewers ask this

Interviewers use Messenger, Instagram, and Twitter designs to test whether you can decouple producers from consumers and scale fan-out to millions of users. They are probing your understanding of delivery guarantees, offline handling, protocol choice, and the fan-out-on-write versus fan-out-on-read trade-off. A strong answer shows you know when pub/sub alone is insufficient and where durable storage or hybrid fan-out is required.

## The core idea

The essence is decoupling: the broker holds subscriptions and routes each published message to all interested subscribers, so adding a subscriber or scaling consumers does not change the publisher. This enables parallel processing and independent scaling, but it moves the reliability burden to the broker and consumers. Delivery is best understood as a spectrum from transient fire-and-forget (Redis Pub/Sub) to durable, replayable logs (Kafka). In feed and chat systems, the central design choice is whether to write the message into every recipient's inbox at publish time (fan-out on write) or compute each recipient's view at read time (fan-out on read), often hybridized by follower count.

## Key points

- Pub-sub decouples publishers from subscribers through a broker and a named topic, enabling one-to-many fan-out without the publisher knowing recipient identities.
- Redis Pub/Sub is strictly in-memory and transient: it provides no persistence, durability, or message replay under any configuration, so messages published while a subscriber is offline are lost.
- Kafka persists messages in a durable, partitioned log and lets consumers replay from committed offsets, so it can serve as a durable pub/sub substrate but is not a drop-in replacement for Redis Pub/Sub.
- Fan-out on write inserts the message into each recipient's inbox at publish time, minimizing read latency at the cost of write amplification; fan-out on read computes the feed from a central timeline, avoiding write amplification but increasing read cost.
- Pure publish-subscribe does not guarantee exactly-once end-to-end delivery; achieving an exactly-once effect requires persistent storage, acknowledgments, retries, deduplication, and idempotent consumers.

## Your 60-second answer

Publish-subscribe is a messaging pattern where publishers send events to a topic, and a broker fans each event out to all subscribers of that topic, without the publisher knowing who receives it. The broker decouples producers from consumers and allows subscribers to scale and process messages independently. The main trade-off is delivery semantics. A transient broker like Redis Pub/Sub keeps no messages on disk, so any subscriber not connected at publish time loses that message permanently. A durable log like Kafka stores messages and lets consumers replay from offsets, but it shifts the API and operational model. For a chat or feed design, I would not rely on pub/sub alone: I'd persist messages in per-user inboxes, push via WebSockets to connected devices, and let offline devices pull missing messages by sequence ID. For celebrities, I'd avoid writing to millions of inboxes and use fan-out on read or a hybrid threshold.

## If they dig deeper

**How do you ensure low-latency message delivery (<100ms) across millions of users?**

Keep persistent WebSocket connections to regional gateway servers, and have those gateways subscribe to user topics on an in-memory broker. Publish to the broker and fan out to only the connection servers holding active sessions, with backpressure and batching; avoid writing to disk on the hot path. Track p95 and p99 latency per region and shed load or degrade to pull-based delivery if the fan-out cannot meet the target.

**What communication protocol will you use: long polling, WebSockets?**

Use WebSockets for bidirectional, low-overhead real-time delivery because the server can push a message immediately. Fall back to long polling where proxies or clients block WebSockets, but long polling adds per-request overhead and latency. HTTP/2 server push is not a reliable replacement because it is tied to a single request-response stream.

**How do you handle offline users and guarantee eventual delivery?**

Persist the message in a durable per-user inbox or outbox before acknowledging the publish, so it is not lost if the subscriber is offline. When a device reconnects, it sends its last seen message ID or timestamp and pulls all missing messages in order. Use idempotent writes and a notification service for mobile devices to wake the app, since WebSockets are not alive in background.

**How do you support multi-device sync so message states are consistent across devices?**

Keep a single source of truth for each user's inbox on the server, with per-device cursors tracking the last message ID each device has seen. Device actions like read receipts update the server state, and the server fans out state changes to other devices via the same pub/sub topic. Reconcile offline edits by last-write-wins or a version vector if concurrent updates need to merge.

**How will you manage group messaging: fan-out on write vs fan-out on read?**

For small groups, fan out on write by inserting the message into each member's inbox, giving low read latency with manageable write amplification. For very large groups or channels, store one copy in a group timeline and let members read it with a cursor, avoiding millions of writes per message. Many systems use a hybrid threshold: fan out on write below a few thousand members and switch to fan-out on read above that, possibly with backfill for active members.

## Worked example

Consider a group chat with 1,000 members. A message service receives a message 'hello' from user A for group G. With fan-out on write, it first writes the message to a messages table with message_id 5001, group_id G, sender A, and timestamp 1700000000, then inserts 1,000 envelope rows into member_inbox(user_id, message_id, received_at). A connected member's device receives the push via its WebSocket gateway; an offline member gets the row persisted and pulls it later by querying member_inbox where user_id = ? and message_id > last_seen. For a 10,000,000-member channel, the same approach would create 10,000,000 envelope rows per message, causing write amplification and storage cost. Fan-out on read stores only the one message and lets members query messages where group_id = G and timestamp > cursor, with an index on (group_id, timestamp); read latency is higher but write cost is constant. A hybrid system can fan out on write for groups under 1,000 members and fan out on read for larger groups.

## Common traps

- Treating Redis Pub/Sub as a durable queue: it discards any message not received by a connected subscriber and has no replay or persistence, regardless of Redis configuration.
- Claiming pub/sub gives exactly-once delivery: without persistent logs, acknowledgments, and idempotent consumers, messages can be lost or duplicated.
- Applying fan-out on write uniformly to accounts with millions of followers (celebrities), which causes write amplification so large it can overwhelm the database and delay publish.
- Ignoring broker failure as a single point of failure and not planning for subscriber reconnection, causing missed messages and stale subscriptions after partitions.

</details>

---

## Fill a code blank (`fill-code-blank` · assemble)

### 66. Executor Framework · Easy

*java · gate confidence 0.8*

<sub>to object to this card: `## java-executor-framework` then `match: Assemble the line that submits a Callable task to an Executo`</sub>

**Question**

Assemble the line that submits a Callable task to an ExecutorService and retrieves its result, using the tokens below. The line should be a single statement that declares a Future and assigns the result of submitting a Callable that returns a String.

**Options**

**Tokens**: executor.submit(() -> "done");, Future<String> future =, Future future =, executor.execute(() -> "done");

**Answer (the reader is graded on)**

- before: 1 → 0

**Reference answer**

Future<String> future = executor.submit(() -> "done");

**Graded on**

- submit() accepts a Callable and returns a Future.
- The lambda () -> "done" is a Callable<String>.
- The Future's type parameter matches the Callable's return type.

<details><summary>The lesson this came from</summary>

The Executor framework in java.util.concurrent separates task submission from execution. Its core Executor interface has execute(Runnable); ExecutorService adds lifecycle management, Future-returning submit methods, and batch invoke methods; ScheduledExecutorService adds delayed and periodic scheduling. ThreadPoolExecutor is the standard implementation, managing a pool of worker threads, a work queue, and configurable rejection policies.

## Why interviewers ask this

The interviewer wants to know whether you can manage concurrency resources correctly instead of spawning raw Thread objects. It tests lifecycle control, queueing, backpressure, and trade-offs around pool sizing, shutdown and exception handling.

## The core idea

A thread pool keeps a bounded number of worker threads alive and reuses them for many short tasks. ThreadPoolExecutor adds a new worker before queueing while the pool is below corePoolSize; once core threads are busy, tasks go to the work queue; only when the queue is full does it create extra threads up to maximumPoolSize. This order means a bounded queue with a max larger than core can absorb bursts, while an unbounded queue can grow without bound. Lifecycle methods plus Future give you control over orderly completion, cancellation, and result retrieval.

## Key points

- Executor.execute(Runnable) returns void; ExecutorService.submit accepts Runnable or Callable and returns a Future for result, cancellation, or completion checks.
- ThreadPoolExecutor creates a new worker before queueing if the pool is below corePoolSize, then queues, then creates up to maximumPoolSize only if the queue is full.
- ThreadPoolExecutor rejects a new task if the executor has been shut down, or if the queue is full and the pool already has maximumPoolSize workers running.
- Executors.newFixedThreadPool uses an unbounded LinkedBlockingQueue, so it never rejects due to queue capacity and can exhaust memory under sustained load.
- shutdown() stops accepting new tasks but lets submitted tasks finish; awaitTermination blocks until that happens or the timeout elapses.

## Your 60-second answer

Java's Executor framework decouples task submission from thread management. Instead of creating a new Thread per task, you submit Runnable or Callable objects to an ExecutorService backed by a thread pool. ThreadPoolExecutor reuses worker threads, queues pending tasks, and manages lifecycle through shutdown and awaitTermination. execute() takes a Runnable and returns void; submit() takes a Runnable or Callable and returns a Future, so you can retrieve a result, check completion, or cancel. A fixed-size pool uses the same number for core and maximum threads, but its default work queue is unbounded, which risks memory exhaustion under load. Tasks are rejected when the executor is shut down or when the queue is full and the pool already has maximum threads running, so the rejection policy should match your backpressure strategy.

## If they dig deeper

**What is the difference between execute() and submit()?**

execute() takes only Runnable and returns void; the task's exception goes to the thread's uncaught exception handler. submit() takes Runnable or Callable and returns a Future, so the caller can get a result, check completion, or cancel; a task exception is thrown from Future.get() wrapped in ExecutionException.

**How does ThreadPoolExecutor decide whether to add a thread or enqueue a task?**

When a task is submitted, if the pool has fewer than corePoolSize workers it creates a new worker. If it is at or above core size, it first tries to enqueue the task. Only if the queue is full and the pool has fewer than maximumPoolSize workers does it create an extra, non-core worker.

**When does ThreadPoolExecutor reject a task?**

It rejects if the executor has been shut down, regardless of queue occupancy. It also rejects when the work queue is full and the pool already has maximumPoolSize threads running. The default AbortPolicy throws RejectedExecutionException; other policies can run the task in the caller, discard it, discard the oldest, etc.

**How do you shut down an ExecutorService correctly?**

Call shutdown() to stop accepting new submissions while allowing queued and running tasks to finish, then call awaitTermination with a timeout and handle the boolean result. shutdownNow() attempts to interrupt running tasks and returns the list of tasks that never started; after either call, verify termination state rather than relying on the method returning.

**Why is the default FixedThreadPool risky under load, and how would you handle backpressure?**

Executors.newFixedThreadPool uses core=max workers and an unbounded LinkedBlockingQueue, so if producers outpace consumers the queue can grow until the heap is exhausted. A safer setup is ThreadPoolExecutor with a bounded queue such as ArrayBlockingQueue and a saturation policy like CallerRunsPolicy, which makes the submitting thread run the task and thereby slows producers.

## Worked example

Consider ThreadPoolExecutor with corePoolSize=2, maximumPoolSize=2, an ArrayBlockingQueue of capacity 1, and the default AbortPolicy. Submit task A and B: both start because worker count is below two. Submit C: the worker count is already two, so C is enqueued. Submit D: the queue is full and worker count equals maximumPoolSize, so reject(D) throws RejectedExecutionException. If you instead call shutdown() before submitting A, then even with an empty queue and zero workers the executor is not accepting tasks, so A is rejected immediately; the queue being full has nothing to do with that rejection.

## Common traps

- Saying a fixed-size pool will reject when its queue fills up ignores that Executors.newFixedThreadPool uses an unbounded LinkedBlockingQueue; ordinary load causes memory growth instead of rejection.
- Assuming shutdown() waits for tasks to complete is wrong: shutdown() only stops new submissions, and you must call awaitTermination to block.
- Treating submit() and execute() as equivalent with exceptions can hide failures; submit captures exceptions in Future.get(), while execute lets them reach the thread's uncaught handler.
- Forgetting to shut down the pool leaves non-daemon worker threads alive and can prevent the JVM from exiting.

</details>

---

### 67. ArrayList vs LinkedList · Easy

*java · gate confidence 0.8*

<sub>to object to this card: `## java-arraylist-vs-linkedlist` then `match: Assemble the line that declares a list variable using the im`</sub>

**Question**

Assemble the line that declares a list variable using the implementation that provides O(1) indexed access. Use all tokens exactly once.

**Options**

**Tokens**: new, List<String>, ArrayList<>();, =, names

**Answer (the reader is graded on)**

- before: 1 → 4 · 4 → 3 · 3 → 0 · 0 → 2

**Reference answer**

The correct line is `List<String> names = new ArrayList<>();`. ArrayList is backed by a resizable array, so `get(int)` computes a direct memory offset and is O(1).

**Graded on**

- ArrayList provides O(1) indexed access because it is backed by an array.
- LinkedList requires O(n) traversal to reach an index.
- The variable is declared as List, the interface both classes implement.

<details><summary>The lesson this came from</summary>

ArrayList stores elements in a contiguous, dynamically resized array; an index read computes a direct memory offset from the base reference. LinkedList stores each element in a separate node carrying item, previous, and next references, so there is no contiguous layout and reaching an index requires following links from the closest end. Both implement List and preserve insertion order; LinkedList additionally implements Deque. Neither class synchronizes its methods.

## Why interviewers ask this

Interviewers ask this to see whether you choose a structure from actual access patterns rather than repeating a table. They test the nuance that 'LinkedList is faster for insert/delete' is only true at the ends or once a node/iterator is positioned, not at an arbitrary index; they also look for understanding of cache locality, memory overhead, and amortized analysis.

## The core idea

The decision comes from memory layout. ArrayList gives O(1) indexed reads and writes because array indexes are offset calculations, and iteration is cache-friendly because elements are adjacent. LinkedList gives O(1) link/unlink for addFirst/addLast/removeFirst/removeLast and for iterator.remove() because the node is already located; inserting at an arbitrary position still costs an O(n) traversal to find that node. At an arbitrary index, both have O(n) cost - ArrayList shifts references, LinkedList follows pointers - so LinkedList has no asymptotic advantage there. Appending to ArrayList is amortized O(1), though growth occasionally copies the array. LinkedList has more per-element memory overhead due to prev/next references, while ArrayList can waste space in unused capacity.

## Key points

- ArrayList is backed by one resizable object array; LinkedList is a doubly linked list of nodes with prev and next references.
- get(int) is O(1) for ArrayList and O(n) for LinkedList because LinkedList traverses from the nearer end.
- Adding or removing at the ends is O(1) for LinkedList; adding at the end is amortized O(1) for ArrayList but occasionally triggers a resize and copy.
- Adding or removing at an arbitrary index is O(n) for both lists: ArrayList shifts elements, LinkedList traverses to the position.
- ArrayList has better cache locality and lower per-element overhead, while LinkedList implements both List and Deque, making it usable as a queue or stack.

## Your 60-second answer

ArrayList is backed by a resizable array; LinkedList is a doubly linked list of nodes. That difference drives the performance. Indexed access is O(1) in ArrayList because get(i) reads a direct array offset. LinkedList get(i) is O(n), walking from the closer end. Insertion and deletion are subtler. Adding or removing at the head or tail of a LinkedList is O(1), which is why its Deque methods are efficient. Adding to the end of an ArrayList is amortized O(1), with an occasional resize copy. At a middle index, both are O(n): ArrayList shifts elements, LinkedList traverses to the node and then links/unlinks. In practice ArrayList usually wins for iteration and random access due cache locality; I default to ArrayList, and pick LinkedList only when the workload is dominated by adding or removing at the ends.

## If they dig deeper

**When would you choose LinkedList instead of ArrayList?**

I would choose LinkedList when the dominating operations are addFirst, removeFirst, addLast, or removeLast - Deque-style work - and random get(i) or heavy iteration is rare. If a queue or stack is needed, I compare it to ArrayDeque: ArrayDeque usually has lower memory overhead and better cache behavior, so I would pick LinkedList mainly when I also need List methods, indexed access in rare cases, or null elements.

**Is LinkedList actually faster for insertion and deletion than ArrayList?**

Only at the ends or through an iterator that already has the node. At an arbitrary index, LinkedList first traverses O(n) to reach the position, then unlinks/links in O(1), so the total is O(n), just like ArrayList's shift. For small or medium list sizes, ArrayList's contiguous copying can beat LinkedList's pointer chasing because of cache locality, so 'LinkedList is faster' is not a universal rule.

**What is the RandomAccess marker interface and how is it used?**

RandomAccess is an empty interface that ArrayList implements and LinkedList does not. JDK algorithms such as Collections.binarySearch and Collections.shuffle check list instanceof RandomAccess; if true they use indexed get/set, otherwise they switch to iterator-based or array-based strategies to avoid accidental O(n^2) behavior on sequential lists.

**How does ArrayList growth work, and why does initial capacity matter?**

In OpenJDK, an ArrayList created with no arguments uses an initial capacity of 10 on first add. When adding would exceed capacity, it allocates a new array about 1.5 times the old length and copies existing references. If the approximate final size is known, supplying an initial capacity avoids repeated allocations; trimToSize can shrink the backing array to the current size.

**What is the complexity of iterator.remove() in ArrayList versus LinkedList, and why?**

ArrayList's iterator.remove() is O(n) because after deleting the element at the cursor, every later reference must be shifted left in the backing array. LinkedList's iterator.remove() is O(1) because the iterator already holds a reference to the current node, so the implementation just unlinks that node by updating its neighbors' prev/next fields.

## Worked example

Consider two lists each holding 100,000 Integer references. `a.get(50_000)` on ArrayList reads one array slot in O(1); `l.get(50_000)` on LinkedList starts at the closer end and follows 50,000 links, O(n). `a.add(0, x)` shifts all 100,000 existing references one slot to the right, O(n); `l.add(0, x)` only allocates a node and updates the head pointer, O(1). `a.add(50_000, x)` shifts 50,000 references; `l.add(50_000, x)` walks 50,000 links then links the node, so both are O(n). The asymmetry is position, not operation name.

## Common traps

- Believing LinkedList is faster than ArrayList for all insertions and deletions; at an arbitrary index it still requires O(n) traversal, and ArrayList's shift can be cheaper due to cache locality.
- Using an indexed for loop with LinkedList because of get(i); repeated get(i) from each iteration causes O(n^2) traversal, while an iterator is O(n).
- Ignoring the RandomAccess marker and choosing algorithms without it; algorithms may degrade on sequential lists.
- Assuming ArrayList end insertion is O(1) worst-case; it is amortized O(1) because resize copies the whole array occasionally.

</details>

---

## Fill a definition (`fill-definition` · assemble)

### 68. Exceptions · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-exceptions` then `match: Assemble the definition of a checked exception in Java by ar`</sub>

**Question**

Assemble the definition of a checked exception in Java by arranging the tokens in the correct order.

**Options**

**Tokens**: not a subclass of, any subclass of, Exception, RuntimeException, that is

**Answer (the reader is graded on)**

- before: 1 → 0 · 0 → 2 · 2 → 4 · 4 → 3

**Reference answer**

A checked exception is any subclass of Exception that is not a subclass of RuntimeException. The compiler forces callers to either catch it or declare it with throws.

**Graded on**

- Checked exceptions are Exception subclasses excluding RuntimeException.
- The compiler enforces handling via catch or throws declaration.
- RuntimeException and Error are unchecked.

<details><summary>The lesson this came from</summary>

Java exception handling is the structured mechanism for throwing and catching java.lang.Throwable subclasses so control transfers from the point of failure to code that can recover or fail cleanly. Throwable has two primary subclasses: Error, for serious JVM-level failures, and Exception, for conditions an application may handle; Exception further splits into RuntimeException and checked exceptions. The compiler forces checked exceptions to be caught or declared, while unchecked exceptions are not enforced. The language constructs are try, catch, finally, throw, and, since Java 7, try-with-resources.

## Why interviewers ask this

The interviewer is testing whether you know the exception hierarchy, the difference between checked and unchecked exceptions, how exceptions propagate, and the rules for overriding methods that declare throws. They also want to see that you handle exceptions without swallowing them or losing the root cause, and that you know when to catch, wrap, or let an exception propagate.

## The core idea

The central distinction is checked versus unchecked. Checked exceptions represent expected, often external conditions—like I/O or database failures—that the compiler forces callers to acknowledge. Unchecked exceptions (RuntimeException and Error) represent programming bugs or serious system failures, so the compiler doesn't force handling. When an exception is thrown, the JVM unwinds the call stack until a matching catch block handles it or the thread terminates; finally blocks and try-with-resources run cleanup during unwinding. Strong exception handling catches only what it can actually handle, preserves the original exception as the cause when wrapping, and avoids broad catch blocks that hide errors.

## Key points

- java.lang.Throwable is the root of the exception hierarchy, with two branches: Error for JVM-level failures and Exception for application-level conditions.
- Checked exceptions—Exception subclasses excluding RuntimeException—must be caught or declared in the method signature; RuntimeException and Error are unchecked.
- When an exception is thrown, the JVM propagates it up the call stack until a matching catch is found or the thread terminates.
- An overriding method may throw the same or a more specific checked exception as the overridden method, but never a broader or new checked exception.
- Since Java 7, try-with-resources auto-closes AutoCloseable resources in reverse declaration order and adds any close failure as a suppressed exception to the primary one.

## Your 60-second answer

In Java, every exception and error inherits from java.lang.Throwable. Throwable has two main branches: Error for serious JVM-level failures such as OutOfMemoryError that you normally don't try to catch, and Exception for conditions your code might be able to handle. Exception splits into RuntimeException and checked exceptions. RuntimeExceptions like NullPointerException are unchecked, meaning they usually indicate programming bugs and don't need to be declared. Checked exceptions like IOException must either be caught or declared in the method signature. When an exception is thrown, the JVM unwinds the call stack looking for a matching catch block; if none is found, the thread terminates. The trade-off is that checked exceptions force callers to handle expected failures, but they can create boilerplate and tight coupling, which is why some newer Java APIs prefer unchecked exceptions.

## If they dig deeper

**What is the difference between checked and unchecked exceptions?**

Checked exceptions are all Exception subclasses except RuntimeException; the compiler forces you to either catch them or declare them with throws. Unchecked exceptions are RuntimeException and its subclasses plus Error, and they require no compile-time handling because they usually indicate programming bugs or JVM failures.

**How does exception propagation work?**

When an exception is thrown, the JVM searches the current method for a matching catch block. If none is found, it unwinds to the caller and repeats the search, continuing up the stack. If no catch is found, the thread terminates and the uncaught exception handler prints the stack trace.

**What are the rules when overriding a method that declares a checked exception?**

The overriding method may throw the same exception, a subclass of it, or no checked exception at all. It cannot throw a broader checked exception or a new checked exception because callers of the supertype only expect to handle the exceptions declared by the supertype method. Unchecked exceptions are not constrained.

**When should you catch an exception versus letting it propagate?**

Catch an exception only when you can handle it, add useful context, or translate it at a module boundary. If you cannot recover, let it propagate or wrap it in a more appropriate exception, preserving the original as the cause. Catching and ignoring a failure is usually worse than crashing.

**How does try-with-resources differ from a finally block when closing resources?**

Since Java 7, try-with-resources automatically closes resources that implement AutoCloseable in reverse order of declaration, even if the try block throws. If both the try body and a close operation throw, the close exception is attached as a suppressed exception to the primary exception, so the original failure is not lost. A manual finally block can easily hide the original exception if close also throws.

## Worked example

Consider a loadConfig() method that calls Files.readString(path) and then Integer.parseInt on a line. Files.readString declares IOException, so loadConfig must either catch it or declare throws IOException. Integer.parseInt throws NumberFormatException, which is unchecked, so no declaration is needed. If the file contains a non-numeric line, parseInt throws NumberFormatException; if loadConfig doesn't catch it and its caller doesn't either, the JVM prints a stack trace showing main -> loadConfig -> parseInt and terminates the thread. If loadConfig instead catches IOException because it cannot recover, it might wrap it in a custom ConfigException with the original IOException as the cause and throw that. The caller can then catch ConfigException and call getCause() to inspect the underlying I/O problem.

## Common traps

- Catching Exception or Throwable broadly can hide programming bugs and serious Errors that should propagate.
- An empty catch block swallows the exception and destroys the evidence of what failed; at minimum log it or rethrow a contextual exception.
- Wrapping an exception without passing the original as the cause loses the root cause, making the stack trace less useful.
- Declaring a broader checked exception in an overriding method does not compile because callers of the supertype cannot see the new exception.

</details>

---

### 69. ArrayList vs LinkedList · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-arraylist-vs-linkedlist` then `match: Assemble the definition of the RandomAccess marker interface`</sub>

**Question**

Assemble the definition of the RandomAccess marker interface and its role in JDK algorithms, using the tokens below. The line should read as a single sentence.

**Options**

**Tokens**: RandomAccess, is, an, empty, marker, interface, that, ArrayList, implements, and, LinkedList, does, not;, JDK, algorithms, such, as, Collections.binarySearch, check, instanceof, RandomAccess, to, choose, indexed, access, for, random-access, lists, and, iterator-based, access, for, sequential, lists.

**Answer (the reader is graded on)**

- before: 0 → 1 · 1 → 2 · 2 → 3 · 3 → 4 · 4 → 5 · 5 → 6 · 6 → 7 · 7 → 8 · 8 → 9 · 9 → 10 · 10 → 11 · 11 → 12 · 12 → 13 · 13 → 14 · 14 → 15 · 15 → 16 · 16 → 17 · 17 → 18 · 18 → 19 · 19 → 20 · 20 → 21 · 21 → 22 · 22 → 23 · 23 → 24 · 24 → 25 · 25 → 26 · 26 → 27 · 27 → 28 · 28 → 29 · 29 → 30 · 30 → 31 · 31 → 32 · 32 → 33

**Reference answer**

RandomAccess is an empty marker interface that ArrayList implements and LinkedList does not; JDK algorithms such as Collections.binarySearch check instanceof RandomAccess to choose indexed access for random-access lists and iterator-based access for sequential lists.

**Graded on**

- RandomAccess is an empty marker interface.
- ArrayList implements RandomAccess; LinkedList does not.
- Algorithms like Collections.binarySearch use instanceof RandomAccess to select an access strategy.
- Indexed access is chosen for RandomAccess lists; iterator-based access for sequential lists.

<details><summary>The lesson this came from</summary>

ArrayList stores elements in a contiguous, dynamically resized array; an index read computes a direct memory offset from the base reference. LinkedList stores each element in a separate node carrying item, previous, and next references, so there is no contiguous layout and reaching an index requires following links from the closest end. Both implement List and preserve insertion order; LinkedList additionally implements Deque. Neither class synchronizes its methods.

## Why interviewers ask this

Interviewers ask this to see whether you choose a structure from actual access patterns rather than repeating a table. They test the nuance that 'LinkedList is faster for insert/delete' is only true at the ends or once a node/iterator is positioned, not at an arbitrary index; they also look for understanding of cache locality, memory overhead, and amortized analysis.

## The core idea

The decision comes from memory layout. ArrayList gives O(1) indexed reads and writes because array indexes are offset calculations, and iteration is cache-friendly because elements are adjacent. LinkedList gives O(1) link/unlink for addFirst/addLast/removeFirst/removeLast and for iterator.remove() because the node is already located; inserting at an arbitrary position still costs an O(n) traversal to find that node. At an arbitrary index, both have O(n) cost - ArrayList shifts references, LinkedList follows pointers - so LinkedList has no asymptotic advantage there. Appending to ArrayList is amortized O(1), though growth occasionally copies the array. LinkedList has more per-element memory overhead due to prev/next references, while ArrayList can waste space in unused capacity.

## Key points

- ArrayList is backed by one resizable object array; LinkedList is a doubly linked list of nodes with prev and next references.
- get(int) is O(1) for ArrayList and O(n) for LinkedList because LinkedList traverses from the nearer end.
- Adding or removing at the ends is O(1) for LinkedList; adding at the end is amortized O(1) for ArrayList but occasionally triggers a resize and copy.
- Adding or removing at an arbitrary index is O(n) for both lists: ArrayList shifts elements, LinkedList traverses to the position.
- ArrayList has better cache locality and lower per-element overhead, while LinkedList implements both List and Deque, making it usable as a queue or stack.

## Your 60-second answer

ArrayList is backed by a resizable array; LinkedList is a doubly linked list of nodes. That difference drives the performance. Indexed access is O(1) in ArrayList because get(i) reads a direct array offset. LinkedList get(i) is O(n), walking from the closer end. Insertion and deletion are subtler. Adding or removing at the head or tail of a LinkedList is O(1), which is why its Deque methods are efficient. Adding to the end of an ArrayList is amortized O(1), with an occasional resize copy. At a middle index, both are O(n): ArrayList shifts elements, LinkedList traverses to the node and then links/unlinks. In practice ArrayList usually wins for iteration and random access due cache locality; I default to ArrayList, and pick LinkedList only when the workload is dominated by adding or removing at the ends.

## If they dig deeper

**When would you choose LinkedList instead of ArrayList?**

I would choose LinkedList when the dominating operations are addFirst, removeFirst, addLast, or removeLast - Deque-style work - and random get(i) or heavy iteration is rare. If a queue or stack is needed, I compare it to ArrayDeque: ArrayDeque usually has lower memory overhead and better cache behavior, so I would pick LinkedList mainly when I also need List methods, indexed access in rare cases, or null elements.

**Is LinkedList actually faster for insertion and deletion than ArrayList?**

Only at the ends or through an iterator that already has the node. At an arbitrary index, LinkedList first traverses O(n) to reach the position, then unlinks/links in O(1), so the total is O(n), just like ArrayList's shift. For small or medium list sizes, ArrayList's contiguous copying can beat LinkedList's pointer chasing because of cache locality, so 'LinkedList is faster' is not a universal rule.

**What is the RandomAccess marker interface and how is it used?**

RandomAccess is an empty interface that ArrayList implements and LinkedList does not. JDK algorithms such as Collections.binarySearch and Collections.shuffle check list instanceof RandomAccess; if true they use indexed get/set, otherwise they switch to iterator-based or array-based strategies to avoid accidental O(n^2) behavior on sequential lists.

**How does ArrayList growth work, and why does initial capacity matter?**

In OpenJDK, an ArrayList created with no arguments uses an initial capacity of 10 on first add. When adding would exceed capacity, it allocates a new array about 1.5 times the old length and copies existing references. If the approximate final size is known, supplying an initial capacity avoids repeated allocations; trimToSize can shrink the backing array to the current size.

**What is the complexity of iterator.remove() in ArrayList versus LinkedList, and why?**

ArrayList's iterator.remove() is O(n) because after deleting the element at the cursor, every later reference must be shifted left in the backing array. LinkedList's iterator.remove() is O(1) because the iterator already holds a reference to the current node, so the implementation just unlinks that node by updating its neighbors' prev/next fields.

## Worked example

Consider two lists each holding 100,000 Integer references. `a.get(50_000)` on ArrayList reads one array slot in O(1); `l.get(50_000)` on LinkedList starts at the closer end and follows 50,000 links, O(n). `a.add(0, x)` shifts all 100,000 existing references one slot to the right, O(n); `l.add(0, x)` only allocates a node and updates the head pointer, O(1). `a.add(50_000, x)` shifts 50,000 references; `l.add(50_000, x)` walks 50,000 links then links the node, so both are O(n). The asymmetry is position, not operation name.

## Common traps

- Believing LinkedList is faster than ArrayList for all insertions and deletions; at an arbitrary index it still requires O(n) traversal, and ArrayList's shift can be cheaper due to cache locality.
- Using an indexed for loop with LinkedList because of get(i); repeated get(i) from each iteration causes O(n^2) traversal, while an iterator is O(n).
- Ignoring the RandomAccess marker and choosing algorithms without it; algorithms may degrade on sequential lists.
- Assuming ArrayList end insertion is O(1) worst-case; it is amortized O(1) because resize copies the whole array occasionally.

</details>

---

## Fill the signature (`fill-signature` · assemble)

### 70. ConcurrentHashMap · Easy

*java · gate confidence 0.8*

<sub>to object to this card: `## java-concurrenthashmap` then `match: Assemble the method signature for ConcurrentHashMap's atomic`</sub>

**Question**

Assemble the method signature for ConcurrentHashMap's atomic compound operation that computes a value for a key only if the key is absent, using the given tokens.

**Options**

**Tokens**: V, computeIfAbsent, (, K, key, ,, Function, <?, super, K, ,, ?, extends, V, >, mappingFunction, ), ;

**Answer (the reader is graded on)**

- before: 0 → 1 · 1 → 2 · 2 → 3 · 3 → 4 · 4 → 5 · 5 → 6 · 6 → 7 · 7 → 8 · 8 → 9 · 9 → 10 · 10 → 11 · 11 → 12 · 12 → 13 · 13 → 14 · 14 → 15 · 15 → 16 · 16 → 17

**Reference answer**

The correct signature is: V computeIfAbsent(K key, Function<? super K, ? extends V> mappingFunction). This method atomically computes a value for the key if it is not already present, returning the existing value if present.

**Graded on**

- computeIfAbsent is a Java 8 atomic compound operation on ConcurrentHashMap.
- It takes a key and a mapping function, returning the value associated with the key.
- The operation is atomic under the per-key lock.

<details><summary>The lesson this came from</summary>

ConcurrentHashMap is a thread-safe implementation of the Map interface in java.util.concurrent, introduced in Java 5. It allows concurrent reads and updates by restricting synchronization to individual hash bins or segments instead of locking the entire map. Iterators are weakly consistent and do not throw ConcurrentModificationException. Null keys and values are rejected with a NullPointerException.

## Why interviewers ask this

Interviewers ask about ConcurrentHashMap to see whether the candidate understands Java concurrency beyond the synchronized keyword. They want to test knowledge of how real-world concurrent data structures reduce contention, the difference between thread safety and scalability, and the guarantees around iteration and compound operations.

## The core idea

The core idea is to avoid a single map-wide lock. In Java 7 the map was split into segments, each guarded by its own ReentrantLock, so writes to different segments could proceed in parallel. In Java 8 the segment design was replaced by lock-free reads and per-bin synchronization using CAS and synchronized blocks on the first node of a bin. Many reads, including get, perform volatile reads without acquiring a lock. Compound operations such as computeIfAbsent and merge are atomic under the per-key lock, giving both safety and scalability.

## Key points

- ConcurrentHashMap rejects null keys and values, throwing NullPointerException immediately.
- Since Java 8, writes lock only the target hash bin; Java 7 used lock striping over a fixed set of segments.
- get and many read operations are lock-free and rely on volatile reads of table references and node fields.
- Iterators are weakly consistent: they traverse some state of the map and never throw ConcurrentModificationException.
- Java 8 added atomic compound operations such as compute, computeIfAbsent, merge, and forEach with parallelism thresholds.

## Your 60-second answer

ConcurrentHashMap is Java's thread-safe map in java.util.concurrent. It gives you concurrent reads and writes without synchronizing the whole map. In Java 8, reads like get are lock-free because internal table references and node fields are volatile, and writes lock only the hash bin being modified, using CAS for insertions. This makes it much more scalable than Hashtable, which synchronizes every method on one lock. Compound operations like computeIfAbsent and merge are atomic under the per-key lock. It does not allow null keys or values, and iterators are weakly consistent, so they won't throw ConcurrentModificationException but may not reflect every concurrent change. The trade-off is that operations such as size or clear can be less globally consistent than under a single global lock, though they are safe.

## If they dig deeper

**How does ConcurrentHashMap differ from Hashtable?**

Hashtable synchronizes every public method on a single lock, which serializes all operations. ConcurrentHashMap allows concurrent reads and writes to different bins; in Java 8, reads are lock-free and writes lock only the bin being modified. Hashtable also rejects null keys and values, but ConcurrentHashMap achieves higher throughput under contention.

**What changed internally between Java 7 and Java 8?**

Java 7 used a fixed number of segments, each with its own ReentrantLock, and the concurrency level set the segment count. Java 8 removed segments and instead uses synchronized on the first node of a hash bin plus CAS for empty-bin insertion, with tree bins for long chains. The constructor's concurrencyLevel parameter is still accepted but used only for initial sizing.

**What does it mean that iterators are weakly consistent?**

An iterator may or may not reflect modifications made after it was created, but it will never throw ConcurrentModificationException. It traverses elements as they existed at some point and reads volatile references, so values reflect up-to-date memory visibility. size may not be exact during concurrent modification.

**Why does ConcurrentHashMap not allow null keys or values?**

In a concurrent map, get returning null is ambiguous: it could mean the key is absent or the value is null. Allowing null values would make containsKey unreliable and complicate atomic remapping methods like computeIfAbsent and merge. Rejecting null removes that ambiguity.

**How does size() work and is it exact during concurrent updates?**

In Java 8, size() sums a base count and counter cells that are updated with CAS, so it does not lock all bins. The returned value is weakly consistent and may not correspond to any single instant if updates happen concurrently. In Java 7, size could lock all segments to compute an exact value, but that was more expensive.

## Worked example

Thread A calls map.computeIfAbsent("user-1", k -> load(k)); Thread B calls map.put("user-2", user2) at the same time. In Java 8 both can proceed because the keys hash to different bins; computeIfAbsent locks only the bin for user-1 and put locks only the bin for user-2. If two threads call computeIfAbsent for the same key, one blocks on the bin lock while the other computes the value. The second thread then sees the value already present and returns it without recomputing, avoiding duplicate initialization. This demonstrates per-key atomicity and bounded locking.

## Common traps

- Saying ConcurrentHashMap locks the entire map: Java 8 locks per hash bin, Java 7 per segment, never the whole map on every operation.
- Assuming its iterators are fail-fast or throw ConcurrentModificationException like HashMap.
- Assuming size() returns an exact global snapshot during concurrent updates.
- Thinking it allows null keys or values because HashMap does; it throws NullPointerException.

</details>

---

### 71. Exceptions · Easy

*java · gate confidence 0.8*

<sub>to object to this card: `## java-exceptions` then `match: Assemble the method signature for a method that reads a file`</sub>

**Question**

Assemble the method signature for a method that reads a file and declares the checked exception it may throw. The method is named readFile, takes a String parameter named path, returns a String, and declares that it throws IOException. Use the tokens below in the correct order.

**Options**

**Tokens**: throws IOException, public, String, readFile, (String path)

**Answer (the reader is graded on)**

- before: 1 → 2 · 2 → 3 · 3 → 4 · 4 → 0

**Reference answer**

The correct signature is: public String readFile(String path) throws IOException. The method declares IOException because it is a checked exception that must be declared in the method signature.

**Graded on**

- Checked exceptions must be declared with throws in the method signature.
- The return type comes before the method name.
- The parameter list is enclosed in parentheses.
- The throws clause comes after the parameter list.

<details><summary>The lesson this came from</summary>

Java exception handling is the structured mechanism for throwing and catching java.lang.Throwable subclasses so control transfers from the point of failure to code that can recover or fail cleanly. Throwable has two primary subclasses: Error, for serious JVM-level failures, and Exception, for conditions an application may handle; Exception further splits into RuntimeException and checked exceptions. The compiler forces checked exceptions to be caught or declared, while unchecked exceptions are not enforced. The language constructs are try, catch, finally, throw, and, since Java 7, try-with-resources.

## Why interviewers ask this

The interviewer is testing whether you know the exception hierarchy, the difference between checked and unchecked exceptions, how exceptions propagate, and the rules for overriding methods that declare throws. They also want to see that you handle exceptions without swallowing them or losing the root cause, and that you know when to catch, wrap, or let an exception propagate.

## The core idea

The central distinction is checked versus unchecked. Checked exceptions represent expected, often external conditions—like I/O or database failures—that the compiler forces callers to acknowledge. Unchecked exceptions (RuntimeException and Error) represent programming bugs or serious system failures, so the compiler doesn't force handling. When an exception is thrown, the JVM unwinds the call stack until a matching catch block handles it or the thread terminates; finally blocks and try-with-resources run cleanup during unwinding. Strong exception handling catches only what it can actually handle, preserves the original exception as the cause when wrapping, and avoids broad catch blocks that hide errors.

## Key points

- java.lang.Throwable is the root of the exception hierarchy, with two branches: Error for JVM-level failures and Exception for application-level conditions.
- Checked exceptions—Exception subclasses excluding RuntimeException—must be caught or declared in the method signature; RuntimeException and Error are unchecked.
- When an exception is thrown, the JVM propagates it up the call stack until a matching catch is found or the thread terminates.
- An overriding method may throw the same or a more specific checked exception as the overridden method, but never a broader or new checked exception.
- Since Java 7, try-with-resources auto-closes AutoCloseable resources in reverse declaration order and adds any close failure as a suppressed exception to the primary one.

## Your 60-second answer

In Java, every exception and error inherits from java.lang.Throwable. Throwable has two main branches: Error for serious JVM-level failures such as OutOfMemoryError that you normally don't try to catch, and Exception for conditions your code might be able to handle. Exception splits into RuntimeException and checked exceptions. RuntimeExceptions like NullPointerException are unchecked, meaning they usually indicate programming bugs and don't need to be declared. Checked exceptions like IOException must either be caught or declared in the method signature. When an exception is thrown, the JVM unwinds the call stack looking for a matching catch block; if none is found, the thread terminates. The trade-off is that checked exceptions force callers to handle expected failures, but they can create boilerplate and tight coupling, which is why some newer Java APIs prefer unchecked exceptions.

## If they dig deeper

**What is the difference between checked and unchecked exceptions?**

Checked exceptions are all Exception subclasses except RuntimeException; the compiler forces you to either catch them or declare them with throws. Unchecked exceptions are RuntimeException and its subclasses plus Error, and they require no compile-time handling because they usually indicate programming bugs or JVM failures.

**How does exception propagation work?**

When an exception is thrown, the JVM searches the current method for a matching catch block. If none is found, it unwinds to the caller and repeats the search, continuing up the stack. If no catch is found, the thread terminates and the uncaught exception handler prints the stack trace.

**What are the rules when overriding a method that declares a checked exception?**

The overriding method may throw the same exception, a subclass of it, or no checked exception at all. It cannot throw a broader checked exception or a new checked exception because callers of the supertype only expect to handle the exceptions declared by the supertype method. Unchecked exceptions are not constrained.

**When should you catch an exception versus letting it propagate?**

Catch an exception only when you can handle it, add useful context, or translate it at a module boundary. If you cannot recover, let it propagate or wrap it in a more appropriate exception, preserving the original as the cause. Catching and ignoring a failure is usually worse than crashing.

**How does try-with-resources differ from a finally block when closing resources?**

Since Java 7, try-with-resources automatically closes resources that implement AutoCloseable in reverse order of declaration, even if the try block throws. If both the try body and a close operation throw, the close exception is attached as a suppressed exception to the primary exception, so the original failure is not lost. A manual finally block can easily hide the original exception if close also throws.

## Worked example

Consider a loadConfig() method that calls Files.readString(path) and then Integer.parseInt on a line. Files.readString declares IOException, so loadConfig must either catch it or declare throws IOException. Integer.parseInt throws NumberFormatException, which is unchecked, so no declaration is needed. If the file contains a non-numeric line, parseInt throws NumberFormatException; if loadConfig doesn't catch it and its caller doesn't either, the JVM prints a stack trace showing main -> loadConfig -> parseInt and terminates the thread. If loadConfig instead catches IOException because it cannot recover, it might wrap it in a custom ConfigException with the original IOException as the cause and throw that. The caller can then catch ConfigException and call getCause() to inspect the underlying I/O problem.

## Common traps

- Catching Exception or Throwable broadly can hide programming bugs and serious Errors that should propagate.
- An empty catch block swallows the exception and destroys the evidence of what failed; at minimum log it or rethrow a contextual exception.
- Wrapping an exception without passing the original as the cause loses the root cause, making the stack trace less useful.
- Declaring a broader checked exception in an overriding method does not compile because callers of the supertype cannot see the new exception.

</details>

---

## Fill the clause (`fill-clause` · assemble)

### 72. Indexes · Medium

*sql · gate confidence 0.8*

<sub>to object to this card: `## sql-indexes` then `match: Assemble the WHERE clause for a query that uses a composite `</sub>

**Question**

Assemble the WHERE clause for a query that uses a composite index on (customer_id, order_date, status) to find shipped orders for customer 42 in the first half of 2024. The clause should let the index seek on customer_id, range scan on order_date, and filter status as a residual predicate.

**Options**

**Tokens**: status = 'shipped', AND order_date BETWEEN '2024-01-01' AND '2024-06-30', WHERE customer_id = 42, AND

**Answer (the reader is graded on)**

- before: 2 → 1 · 1 → 3 · 3 → 0

**Reference answer**

The correct clause is: WHERE customer_id = 42 AND order_date BETWEEN '2024-01-01' AND '2024-06-30' AND status = 'shipped'. This order places the equality column first for the seek, the range column second for the scan, and the residual predicate last, matching the composite index key order.

**Graded on**

- Equality column customer_id comes first to enable an index seek.
- Range column order_date comes second to bound the index scan.
- status is applied last as a residual filter and cannot narrow the seek range.
- The column order in the WHERE clause should match the composite index key order for optimal use.

<details><summary>The lesson this came from</summary>

An index is a separate data structure, usually a B-tree, that stores a sorted copy of one or more columns from a database table plus a pointer to the row the values came from. It lets the query planner seek or range-scan on key columns instead of scanning the entire table. Engines differ in clustering: SQL Server has one clustered index that determines physical row order and non-clustered indexes as separate B-trees; MySQL InnoDB always clusters by the primary key; PostgreSQL stores table rows in an unordered heap and all standard indexes are secondary.

## Why interviewers ask this

Interviewers use indexes to test whether you understand real database performance, not just syntax. They want to see you can choose a good index for a given query, reason about composite key order and covering indexes, and explain the write/storage tradeoff. Many candidates can recite CREATE INDEX but cannot predict when an index helps or hurts.

## The core idea

An index is a copy of data organized for search: it speeds up reads because the engine can walk a B-tree instead of scanning every row, but it adds storage and every insert/update/delete must keep the copies in sync. Composite indexes work left-to-right: equality columns position the seek, a range column bounds the scan, and later columns cannot narrow the seek range but can still be applied as predicates inside the index scan before row lookups in engines that support index condition pushdown. Write cost is engine-dependent: in PostgreSQL's append-only MVCC, an UPDATE creates a new tuple version and unless HOT optimization applies, all secondary indexes on the table receive entries for the new version, even when no indexed column changed.

## Key points

- Most general-purpose SQL indexes are B-trees that support O(log n + rows returned) seeks and range scans, compared with O(n) full table scans.
- A composite index on (a, b, c) can only be used efficiently for lookups that include leading columns; a query filtering only on b or c usually cannot use that index for a seek.
- For a WHERE clause with equality on a and range on b, c cannot narrow the seek range, but engines such as MySQL, SQL Server, PostgreSQL and Oracle can still apply c as an index filter while scanning the index.
- In SQL Server, clustered indexes define physical row order and are limited to one per table; MySQL InnoDB always has a clustered primary key; PostgreSQL has no clustered indexes and stores rows in a heap with secondary indexes pointing to row locations.
- In PostgreSQL's MVCC, an UPDATE writes a new tuple version and, unless HOT is possible on the same page, all secondary indexes are updated to point to the new version even if the updated columns are not part of any index.

## Your 60-second answer

A database index is a separate data structure, typically a B-tree, that keeps a sorted copy of one or more columns and pointers to the corresponding rows. It lets the optimizer find rows by seeking or scanning a small range instead of reading the whole table. In exchange, indexes consume storage and write operations must keep them in sync, so write-heavy tables can slow down significantly. How the columns are ordered matters: for a composite index, equality columns must come before range columns, and any column after the range cannot narrow the seek but can still be applied as a filter during the index scan in modern engines. Clustered indexes, where supported, define the table's physical order; non-clustered indexes are separate structures.

## If they dig deeper

**What are the main costs of creating too many indexes?**

Each index duplicates the key columns and adds storage. Writes must update indexes, increasing insert/update/delete latency. In MVCC engines like PostgreSQL, even updating a non-indexed column can force writes to every secondary index unless HOT optimization is possible on the same page.

**Given an index on (a, b, c) and WHERE a = 1 AND b > 2 AND c = 3, how much of the index is used?**

The B-tree can use a as an equality seek and then range scan b > 2. C cannot narrow the start or end of that b range because the index is sorted first by a, then b, so c values are not consecutive for all b > 2. Modern engines such as MySQL, SQL Server, PostgreSQL and Oracle still apply c as a residual predicate inside the index scan, avoiding base table lookups for rows that fail c = 3.

**Explain the difference between clustered and non-clustered indexes.**

A clustered index determines the physical order of table rows; SQL Server allows at most one per table and the leaf level is the data pages. MySQL InnoDB always stores rows in the primary key's clustered B-tree, with secondary indexes holding primary key values to find rows. PostgreSQL has no clustered index concept in its normal storage: rows live in an unordered heap, and every index, including the primary key, is a secondary structure pointing to row locations.

**Why does PostgreSQL update every secondary index when you change a non-indexed column?**

PostgreSQL uses MVCC: an UPDATE does not overwrite the old row, it writes a new physical tuple version. Every secondary index entry points to the physical tuple location, so the database must add entries for the new version into all indexes on the table. The HOT optimization avoids this only when the new tuple fits on the same heap page and no indexed column changes; then old index entries can be redirected via the line pointer, so secondary indexes remain unchanged.

## Worked example

Take an orders table with columns customer_id, order_date, status, and amount, and an index on (customer_id, order_date, status). A query asks: SELECT * FROM orders WHERE customer_id = 42 AND order_date BETWEEN '2024-01-01' AND '2024-06-30' AND status = 'shipped'. The B-tree descends to customer_id 42, then scans the order_date range as a contiguous block. Because the next key column status comes after order_date, it cannot start the scan at the first 'shipped' row inside that range; the scan visits all rows with order_date in that range. With index condition pushdown, the engine evaluates status = 'shipped' on the index entries and only performs base table lookups for rows that pass, avoiding I/O for rows that do not match. Without ICP, every row in the order_date range would trigger a lookup to check status.

## Common traps

- Believing an index on (a,b,c) can speed up a query that filters only on b or c; without leading column a, the B-tree cannot provide a direct seek.
- Over-indexing because each index helps a read; on a write-heavy table, the accumulated index maintenance can dominate and even hurt overall workload.
- Assuming 'c' is useless after a range on 'b' in a composite index; it cannot narrow the seek range but can still be used as an index filter before table access.
- Confusing clustered with unique: a clustered index concerns physical storage order, while a unique index is a constraint that rejects duplicate key values.

</details>

---

### 73. Clustered vs non-clustered indexes · Medium

*sql · gate confidence 0.9*

<sub>to object to this card: `## sql-clustered-vs-non-clustered-indexes` then `match: Assemble the SQL Server statement that creates a non-clustered index on the CustomerID column of the Orders table, including the OrderDate and Amount columns as included columns to make the index cove`</sub>

**Question**

Assemble the SQL Server statement that creates a non-clustered index on the CustomerID column of the Orders table, including the OrderDate and Amount columns as included columns to make the index covering for queries that filter on CustomerID and select OrderID, OrderDate, and Amount. Assume the table has a clustered primary key on OrderID.

**Options**

**Tokens**: INCLUDE (OrderDate, Amount), CREATE NONCLUSTERED INDEX IX_Orders_CustomerID, ON Orders (CustomerID), ;

**Answer (the reader is graded on)**

- before: 0 → 1 · 1 → 2 · 2 → 3

**Reference answer**

CREATE NONCLUSTERED INDEX IX_Orders_CustomerID ON Orders (CustomerID) INCLUDE (OrderDate, Amount); The INCLUDE clause adds the non-key columns to the leaf level of the non-clustered index, so the query can be served entirely from the index without a key lookup to the clustered index.

**Graded on**

- The INCLUDE clause adds non-key columns to the leaf level of a non-clustered index.
- Included columns are not part of the index key and do not affect the order of index entries.
- A covering index eliminates key lookups for queries that select only the indexed and included columns.
- The clustering key (OrderID) is automatically included in the non-clustered index as the row locator.

<details><summary>The lesson this came from</summary>

A clustered index determines the physical order of data rows in a table; the leaf level of its B-tree contains the actual rows, so a table can have only one. A non-clustered index is a separate B-tree whose leaf nodes hold the indexed key values plus a row locator: the clustering key if the table has a clustered index, or a row ID if the table is a heap.

## Why interviewers ask this

The interviewer is testing whether you understand how indexes are physically stored and how that affects query performance. They want to see you know the trade-offs between faster reads and slower writes, and that a non-clustered index does not always eliminate table access.

## The core idea

A clustered index is the table itself, not an extra copy: sorting the leaf pages means the data rows are physically ordered by the clustering key. A non-clustered index is an auxiliary structure that stores the indexed columns plus a pointer back to the row. On a heap, that pointer is a row ID; on a clustered table, it is the clustering key, which makes the clustering key part of every non-clustered index. When a query needs columns outside a non-clustered index, SQL Server performs a key lookup through the clustered index for each matching row. Adding those columns to the non-clustered index with INCLUDE creates a covering index and eliminates the key lookup, but widens the index and increases write overhead.

## Key points

- In SQL Server, a table can have at most one clustered index because the leaf level of its B-tree is the actual data rows in key order; a primary key defaults to clustered unless specified otherwise.
- Non-clustered indexes are separate B-trees; their leaf nodes store the indexed key columns plus a row locator, which is the clustering key for a clustered table or a row ID for a heap.
- On a table with a clustered index, a non-clustered seek that needs columns outside the index performs a key lookup through the clustered index for each row, which can dominate query cost.
- Adding required columns to a non-clustered index with INCLUDE creates a covering index and removes key lookups for those queries.
- Indexes speed up reads but slow writes because every insert, update, or delete must maintain all affected index structures.

## Your 60-second answer

A clustered index determines the physical order of rows in a table; the leaf level of its B-tree is the data itself, so there can be only one per table. In SQL Server, a primary key defaults to being the clustered index. A non-clustered index is a separate B-tree whose leaf nodes store the indexed key values and a row locator. If the table has a clustered index, that locator is the clustering key; if it's a heap, it's a row ID. Reads that can be served entirely from the non-clustered index avoid extra lookups. When they need columns outside the index, SQL Server performs a key lookup, traversing the clustered index per row, which can become expensive. The trade-off is that every index speeds up reads but adds maintenance on every insert, update, and delete.

## If they dig deeper

**What is stored at the leaf level of a clustered index?**

The actual data rows of the table, sorted by the clustered index key. That's why a table can have only one clustered index: the rows cannot be physically in two orders at once without duplicating the table.

**When a table has a clustered index, what does a non-clustered index leaf page contain?**

The non-clustered index key columns plus the clustered index key as the row locator. For example, if Orders is clustered on OrderID and has a non-clustered index on CustomerID, each leaf entry is (CustomerID, OrderID). The engine uses OrderID to key lookup the full row when needed.

**What causes a key lookup in an execution plan, and what would you change to remove it?**

A key lookup happens when a non-clustered index seek is used, but the query requests columns not included in that index. SQL Server fetches the missing columns by traversing the clustered index for each matching row using the clustering key. To eliminate it, add the missing columns to the non-clustered index with INCLUDE, making it covering, or narrow the SELECT list.

**How does index fragmentation differ between clustered and non-clustered indexes, and when would you rebuild versus reorganize in SQL Server?**

Fragmentation makes pages logically out of order or partially empty, hurting range scans. For a clustered index fragmentation affects the table's data pages directly; for a non-clustered index it affects only the B-tree pages. In SQL Server, Microsoft's general guidance is reorganize for fragmentation roughly 5-30% and rebuild above 30%, with rebuild being more thorough but heavier.

## Worked example

Consider an Orders table clustered on OrderID with a non-clustered index on CustomerID, created without INCLUDE columns. Query: SELECT OrderID, OrderDate, Amount FROM Orders WHERE CustomerID = 123. The engine seeks the non-clustered index, finds entries (CustomerID=123, OrderID). But OrderDate and Amount are not in that index, so for each matching OrderID it performs a key lookup into the clustered index to fetch those columns. If instead the index is created with INCLUDE(OrderDate, Amount), each leaf entry contains CustomerID, OrderID, OrderDate, and Amount. The seek returns all requested columns; the optimizer marks the query covered and no key lookup appears. The trade-off is a wider index that consumes more storage and write overhead.

## Common traps

- Saying a non-clustered index stores a physical RID for every table; when a clustered index exists, the row locator is the clustered key, so updates to the clustering key must propagate to all non-clustered indexes.
- Assuming the primary key is always clustered; SQL Server makes it the default but you can define a nonclustered primary key and cluster on a different column, such as a date column for range scans.
- Creating a non-clustered index on every frequently filtered column without considering write traffic; every insert, update, and delete must maintain additional index structures, which can degrade write throughput.
- Recommending a SQL Server rebuild threshold as if it applies to MySQL or PostgreSQL; fragmentation handling and index behavior differ across engines.

</details>

---

## Flash (`flash` · self_rate)

### 74. Recursive CTEs · Easy

*sql · gate confidence 0.7*

<sub>to object to this card: `## sql-recursive-ctes` then `match: Do you know what the anchor member of a recursive CTE does?`</sub>

**Question**

Do you know what the anchor member of a recursive CTE does?

**Reference answer**

The anchor member is the non-recursive query that returns the initial rows, usually the roots of the hierarchy.

**Graded on**

- Anchor member is non-recursive.
- It seeds the initial rows.
- Typically selects root nodes.

<details><summary>The lesson this came from</summary>

A recursive CTE is a common table expression that references its own name, allowing SQL to process rows iteratively. It is built from an anchor member returning the initial rows and a recursive member that joins the previous result to further rows. The engine repeatedly evaluates the recursive member until no rows are produced or an engine-specific recursion limit stops execution. Recursive CTEs are the standard declarative technique for walking adjacency-list hierarchies such as org charts, trees, bills of materials, and threaded comments.

## Why interviewers ask this

Interviewers use recursive CTEs to test whether you can translate a hierarchical business requirement into SQL without procedural loops. They also check that you understand iterative execution, termination conditions, and engine-specific syntax, because a wrong syntax or unlimited recursion is an immediate failure in a live coding session. Questions often ask for an org chart, all descendants of a manager, or a generated date series.

## The core idea

A recursive CTE is essentially a declarative loop: the anchor seeds a working set, and the recursive member adds rows by joining the base table to the rows produced in the previous iteration. The database repeats that recursive step one iteration at a time, not all at once. UNION ALL preserves every row and can duplicate paths; UNION (DISTINCT) eliminates exact duplicate rows and can terminate some cyclic walk cases. SQL Server and Oracle only allow UNION ALL for recursion, while PostgreSQL, SQLite, MySQL, and standard SQL also accept UNION. Because each recursive step sees only the previous batch, the recursive member cannot sensibly perform aggregation or windowing across the whole result.

## Key points

- A recursive CTE must be written with WITH RECURSIVE in PostgreSQL, MySQL 8.0+, and SQLite, while SQL Server and Oracle use plain WITH without the RECURSIVE keyword.
- SQL Server and Oracle require UNION ALL in recursive CTEs; PostgreSQL, SQLite, MySQL, and the SQL standard support both UNION ALL and UNION (DISTINCT), where UNION can eliminate exact duplicate rows.
- The anchor member returns the initial rows, and the recursive member references the CTE name to produce the next level from the previous iteration.
- Termination comes from the recursive member returning no rows, or from limits such as SQL Server's default 100 recursions or MySQL's cte_max_recursion_depth of 1000.
- Most engines disallow aggregate functions, window functions, GROUP BY, and DISTINCT inside the recursive member because each iteration sees only the previous batch.

## Your 60-second answer

A recursive CTE is a CTE that references itself. It has an anchor query that seeds the first rows and a recursive query that references the CTE to generate the next iteration. The database joins the previous result to the base table over and over until no new rows come back or a recursion limit is hit. Use UNION ALL to keep every row. In PostgreSQL, SQLite, MySQL, and standard SQL you can also use UNION to drop duplicate rows and help stop some cyclic walks, but SQL Server and Oracle require UNION ALL. This is the standard declarative way to walk an adjacency list like an org chart, bill of materials, or comment threads. The main trade-off is level-by-level execution: indexes on the parent column matter, and cycles or deep hierarchies can be expensive or hit the limit.

## If they dig deeper

**What is the difference between the anchor member and the recursive member?**

The anchor member is a non-recursive query that returns the starting rows, usually the roots of the hierarchy. The recursive member references the CTE name and joins the previous iteration's rows to the base table to produce the next level. Together they set the base case and the step that repeats until termination.

**How would you write a query to get all descendants of a specific employee?**

The anchor selects the starting employee by ID. The recursive member joins employees whose manager_id equals the CTE's current employee_id, adding each child with an incremented level or path. This repeats until no further children are found, returning the complete subtree.

**What happens if the data contains a cycle, and how do you prevent infinite recursion?**

With UNION ALL, cyclic parent-child links make each iteration produce the same rows again, so the query runs until the engine's recursion limit or an error. You can stop it by using UNION to eliminate exact duplicate rows, by tracking a visited path such as an array or delimited string and filtering out seen IDs, or by setting a max recursion limit as a backstop.

**What restrictions apply inside the recursive member, and why?**

Most engines forbid aggregate functions, window functions, GROUP BY, and DISTINCT inside the recursive member. The reason is that each iteration is fed only the previous batch of rows, not the accumulated result, so multi-row aggregation would be ill-defined. The top-level set operator may still be UNION DISTINCT where the engine supports it, but that operates on the union of anchor and recursive results, not as an internal group-by.

## Worked example

Consider an employees table with rows (1, 'Alice', NULL), (2, 'Bob', 1), (3, 'Carol', 1), and (4, 'Dave', 2), where the third column is manager_id. The anchor SELECT id, name, manager_id, 0 AS level FROM employees WHERE manager_id IS NULL returns Alice at level 0. The recursive member SELECT e.id, e.name, e.manager_id, o.level + 1 FROM employees e JOIN org o ON e.manager_id = o.id first joins against Alice, producing Bob and Carol at level 1. It then runs against Bob and Carol, producing Dave at level 2. The next iteration finds no employees managed by Dave, so execution stops and the result contains Alice, Bob, Carol, and Dave in that order.

## Common traps

- Using WITH RECURSIVE on SQL Server or Oracle: both use plain WITH, and SQL Server and Oracle will reject the RECURSIVE keyword.
- Assuming UNION ALL is required everywhere: PostgreSQL, SQLite, MySQL, and the SQL standard allow UNION, and blindly using UNION ALL on cyclic data can loop until the limit.
- Placing aggregate functions, window functions, or an internal DISTINCT inside the recursive member, which most engines reject because the recursive step sees only the previous batch.
- Forgetting to set or understand the recursion limit, then being surprised when a deep hierarchy fails with SQL Server's default of 100 or MySQL's cte_max_recursion_depth limit.

</details>

---

### 75. NoSQL types · Easy

*system_design · gate confidence 0.7*

<sub>to object to this card: `## sd-nosql-types` then `match: Name the four main NoSQL data models.`</sub>

**Question**

Name the four main NoSQL data models.

**Reference answer**

The four main NoSQL data models are key-value, document, wide-column, and graph.

**Graded on**

- Key-value stores map unique keys to opaque values.
- Document stores store JSON/BSON documents and index fields inside them.
- Wide-column stores group data into column families under a row/partition key.
- Graph stores model entities as nodes and relationships as first-class edges.

<details><summary>The lesson this came from</summary>

NoSQL types are distinct data models rather than one uniform store. Key-value stores map unique keys to opaque values, usually as a hash table on memory or disk; document stores store JSON/BSON documents as values and index fields inside them; wide-column stores group data into column families under a row/partition key; graph stores model entities as nodes and relationships as first-class edges. They denormalize data and move joins into application code.

## Why interviewers ask this

Interviewers test whether candidates map access patterns to the right data model instead of defaulting to relational tables. Questions about designing key-value stores or document systems then shift to partitioning, replication, fault tolerance, and consistency. A strong answer names the operations each model makes cheap and where it fails.

## The core idea

Choose by access pattern: exact key reads and writes fit key-value; self-contained documents with field queries fit document stores; write-heavy rows with a known partition key and ordered ranges fit wide-column; relationship traversal fits graph. The models optimize different layers: key-value optimizes lookup, document adds field indexes, wide column adds partition-local ordering, and graph adds adjacency for local traversals. As a result, denormalization and application-side joins are normal. A model that is efficient for one query pattern can be poor for an unplanned query.

## Key points

- A key-value store gives O(1) average get/put by key, but values are opaque; filtering, scanning, or secondary queries must be implemented in the application or by another index.
- A document store is a key-value store whose values are JSON/BSON documents and can be indexed by internal fields, so it supports both point lookups and field-level queries.
- In a wide-column store like Cassandra, the primary key's partition key determines which node owns the row, and clustering columns define an order for efficient range scans within that partition.
- In Neo4j's index-free adjacency, moving from a known node to its neighbors avoids global index lookups, but the work is proportional to that node's degree rather than strictly O(1).
- NoSQL systems often use BASE and eventual consistency, but many support ACID or tunable consistency: Cassandra has per-query consistency levels, MongoDB supports multi-document transactions, and Neo4j is ACID at the graph operation level.

## Your 60-second answer

There are four main NoSQL models: key-value, document, wide-column, and graph. Key-value stores like Redis or DynamoDB provide O(1) average lookups by key, so they fit caches, sessions, and feature flags. Document stores like MongoDB store JSON or BSON values and index fields inside them, so they fit catalogs and content management. Wide-column stores like Cassandra or Bigtable group data into column families under a partition key and are built for high write throughput and partition-local range scans, so they fit sensor data and time-series events. Graph databases like Neo4j store relationships as first-class edges and traverse them in time proportional to the degree of the current node, so they fit social networks and recommendation engines. The tradeoff is denormalization and application-side joins, plus relaxed global consistency in many of these systems.

## If they dig deeper

**What are the four NoSQL data models and one common use case for each?**

Key-value stores support exact-key lookups and fit caches or sessions; document stores fit applications with self-contained JSON/BSON records and field queries; wide-column stores fit write-heavy workloads that scan by a known partition key; graph databases fit social graphs, fraud detection, and recommendation traversal.

**How do you decide between a key-value store and a document store?**

If the application only ever retrieves by a single key and the value can be opaque, a key-value store is enough. If it needs to query, index, or update fields inside the value, a document store is the natural next step because it adds field-level indexes on JSON/BSON documents.

**How does a wide-column data model differ from a relational table?**

A wide-column table is sparse, with a row partitioned by partition key and ordered by clustering columns; columns within a column family can vary per row. It does not provide general SQL joins and performs best when queries follow the partition key, whereas relational tables normalize and join across tables.

**How does Neo4j's graph traversal actually perform?**

Neo4j uses index-free adjacency, so moving from a node to a relationship bypasses a global index lookup. However, finding which of that node's edges match a type or target is proportional to the number of relationships connected to the node, not to the total graph size.

**How would you distribute a key-value store and make it fault tolerant? Is it CP or AP?**

Partition keys with consistent hashing and replicate each key to multiple nodes. Use quorum reads and writes: R+W>N means a read and write see at least one shared replica, but you still need version vectors or timestamps to resolve concurrent or failed writes. Many key-value stores are AP with eventual consistency, while others are tunable or CP depending on quorum configuration.

## Worked example

Take a replicated key-value store with replication factor N=3. Key user:42 is placed on replicas P, P+1, and P+2 by consistent hashing. A write coordinator sends the new value to all three replicas and returns success after W=2 of them acknowledge the write. A later read with R=2 contacts any two replicas; because R+W=4 is greater than N=3, at least one replica in that read saw the latest write. If two coordinators wrote different values concurrently, the read must compare version vectors and return the value that causally wins. If a write is acknowledged by only one replica and that replica fails before propagating, a later read can observe stale data. Quorums therefore give intersection, not automatic linearizability.

## Common traps

- Assuming key-value stores can filter or query values; they only provide efficient access by key unless you build an extra index or scan in application code.
- Treating a wide-column store as a relational table and expecting joins or arbitrary secondary indexes; queries that do not follow the partition key can become full-cluster scans.
- Claiming Neo4j traversal is O(1) per hop regardless of node degree; actual cost is proportional to the relationships attached to the current node.
- Saying all NoSQL is eventually consistent or cannot be ACID; Cassandra has tunable consistency, MongoDB supports multi-document transactions, and Neo4j is ACID at the graph operation level.

</details>

---

## Complexity table (`complexity-table` · grid_toggle)

### 76. Java 8 Features · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-java-8-features` then `match: Select the cells that correctly describe Java 8 features. Ro`</sub>

**Question**

Select the cells that correctly describe Java 8 features. Rows are features, columns are descriptions.

**Options**

**Columns**: Implement functional interfaces, Lazy evaluation with terminal operations, Model absence of a value, Allow interface evolution without breaking implementers
**Rows**: Lambda expressions, Stream API, Optional, Default methods

**Answer (the reader is graded on)**

- Ticked: Lambda expressions · Implement functional interfaces, Stream API · Lazy evaluation with terminal operations, Optional · Model absence of a value, Default methods · Allow interface evolution without breaking implementers

**Reference answer**

Lambda expressions implement functional interfaces, the Stream API is lazy and requires a terminal operation, Optional models absence of a value, and default methods allow interfaces to evolve without breaking implementers.

**Graded on**

- Lambda expressions are shorthand for instances of functional interfaces.
- Streams are lazy; intermediate operations do nothing until a terminal operation runs.
- Optional is a container for at most one value, replacing null-returning conventions.
- Default methods let interfaces add new methods without breaking existing implementers.

<details><summary>The lesson this came from</summary>

Java 8 is a major Java release that introduced functional programming support through lambda expressions, method references, and the Stream API. It also added default and static methods in interfaces, the Optional class for modelling absent values, a new immutable and thread-safe date/time API (java.time), Base64 encoding/decoding utilities, and new Map methods such as putIfAbsent and compute. These changes enabled more declarative, less boilerplate-heavy code.

## Why interviewers ask this

Interviewers want to see whether a candidate has moved past Java 7 idioms and can use lambdas, streams, and Optional correctly. Many production codebases still run on Java 8 or were modernised to it, so understanding these features is a baseline for reading and writing modern Java. The questions also probe comprehension of lazy evaluation, functional interfaces, and backward-compatible API evolution.

## The core idea

Java 8's core shift is from external, imperative iteration over collections to internal, declarative stream pipelines driven by lambda expressions. A lambda is a concise implementation of a functional interface; method references are even more compact. Streams are lazy pipelines that do not store data, and intermediate operations only define transformations while terminal operations execute them. Optional replaces null-returning conventions with a type-level signal of absence, but it does not eliminate all exceptions if get() is misused. Default methods allow interfaces to gain new methods, such as Collection.stream(), without breaking existing implementers.

## Key points

- A lambda expression is shorthand for an instance of a functional interface, which has exactly one abstract method.
- The Stream API provides lazy internal iteration; intermediate operations like filter and map return a stream, and only a terminal operation like collect or reduce starts processing.
- Java 8's java.time package contains immutable, thread-safe classes such as LocalDate, LocalTime, LocalDateTime, and ZonedDateTime, replacing mutable Date and Calendar.
- Optional is a container for at most one value; calling get() on an empty Optional throws NoSuchElementException, so orElse/orElseGet/ifPresent are preferred.
- Default and static methods in interfaces enable API evolution without breaking implementers; this is how stream() was added to the Collection interface.

## Your 60-second answer

Java 8's most significant features are lambda expressions, the Stream API, and the new date/time API. Lambdas let you pass behaviour as data by concisely implementing functional interfaces, and the Stream API uses them for declarative bulk operations on collections. Streams are lazy pipelines: filter and map define the pipeline, but nothing runs until a terminal operation like collect or reduce is called. Java 8 also introduced Optional to model the absence of a value more explicitly than null, default methods in interfaces so that existing code can evolve without breaking implementers, and the java.time package with immutable, thread-safe date and time classes. The main trade-off is that functional-style code can become hard to debug, and misusing Optional.get can still produce exceptions if you don't check presence first.

## If they dig deeper

**What is a functional interface in Java 8?**

An interface with exactly one abstract method. It can include default and static methods. Examples are Runnable, Callable, Comparator, and the functional interfaces in java.util.function such as Predicate, Function, Consumer, and Supplier. The @FunctionalInterface annotation is optional but lets the compiler enforce the single abstract method rule.

**How do streams differ from collections?**

Collections are in-memory data structures that store elements; streams are lazy pipelines over a data source that do not store data. Streams support internal iteration using lambda expressions, can represent infinite sequences, and are consumed once after a terminal operation. Intermediate operations return a new stream and defer execution until a terminal operation runs.

**What is the difference between map and flatMap in Streams?**

map applies a one-to-one transformation, producing exactly one output per input element. flatMap applies a one-to-many transformation, where each input produces a stream of zero or more outputs, and then flattens those nested streams into a single stream. flatMap is useful for flattening nested collections or Optional values.

**Why were default methods added to interfaces, and what diamond problem can they cause?**

Default methods let interfaces evolve by adding new methods with an implementation without forcing every implementing class to add code; this is how Collection gained stream() in Java 8. The diamond problem occurs when a class implements two interfaces that provide conflicting default methods for the same signature. In that case the class must override the method, and can explicitly call a specific interface's default using InterfaceName.super.method().

**How does Optional prevent null-related errors, and what are the pitfalls of get()?**

Optional wraps a value or signals its absence, forcing callers to handle the absent case explicitly. In Java 8, safe access is via isPresent, ifPresent, orElse, orElseGet, and orElseThrow; calling get on an empty Optional throws NoSuchElementException, so it should only follow an isPresent check. ifPresentOrElse, which handles both present and absent side effects, was introduced later in Java 9.

## Worked example

Consider finding the sum of squares of even numbers in a list. In Java 8, write `List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5); int result = numbers.stream().filter(n -> n % 2 == 0).map(n -> n * n).reduce(0, Integer::sum);`. The filter step keeps 2 and 4; map squares them to 4 and 16; reduce starts at 0 and adds them, producing 20. Because filter and map are lazy, no work happens until reduce runs. If you removed reduce and assigned the stream to a variable, the pipeline would be defined but not executed.

## Common traps

- Calling Optional.get() without checking isPresent(); an empty Optional throws NoSuchElementException, and Java 8 does not have ifPresentOrElse to handle both sides in one method.
- Forgetting that streams are lazy: a chain of intermediate operations alone never processes any elements; a terminal operation is required.
- Treating a stream as reusable: after a terminal operation the stream is consumed, and trying to operate on it again throws IllegalStateException.
- Using map where flatMap is needed: map cannot flatten one-to-many transformations, leading to nested streams or incorrect types.

</details>

---

### 77. OOP Concepts · Medium

*java · gate confidence 0.8*

<sub>to object to this card: `## java-oop-concepts` then `match: Consider a standard Java implementation of these OOP feature`</sub>

**Question**

Consider a standard Java implementation of these OOP features. Select every cell that correctly pairs the feature with its runtime/compile-time behavior.

**Options**

**Columns**: Compile-time resolution, Runtime resolution
**Rows**: Overloaded methods, Overridden methods, Interface default methods, Static methods

**Answer (the reader is graded on)**

- Ticked: Overloaded methods · Compile-time resolution, Overridden methods · Runtime resolution, Interface default methods · Runtime resolution, Static methods · Compile-time resolution

**Reference answer**

Overloaded methods are resolved at compile time based on argument types, while overridden methods are resolved at runtime based on the object's actual class. Interface default methods are resolved at runtime through dynamic dispatch, and static methods are resolved at compile time based on the reference type.

**Graded on**

- Overloading is compile-time resolution based on argument types.
- Overriding uses runtime dynamic dispatch on the object's class.
- Default methods are dispatched dynamically like instance methods.
- Static methods are resolved at compile time from the reference type.

<details><summary>The lesson this came from</summary>

Object-oriented programming organizes code into classes that bundle state (fields) with behavior (methods). In Java, classes act as blueprints, instance fields hold per-object state, and methods operate on that state. The four core principles are encapsulation (restricting access to internal state), inheritance (subclassing a parent type), polymorphism (dispatching calls based on the actual object's runtime type), and abstraction (exposing only essential behavior through abstract classes and interfaces).

## Why interviewers ask this

Interviewers use OOP questions to test whether you can design cohesive classes, protect invariants with access control, and explain runtime dispatch versus compile-time resolution. They also probe Java-specific mechanics—single inheritance, interfaces, Object methods, and where Java is not purely object-oriented—so a candidate who only recites definitions fails. Strong answers connect each principle to a concrete Java feature or failure mode.

## The core idea

OOP binds data and the operations on it into one unit, so an object's state changes only through its methods. Encapsulation is enforced in Java with access modifiers: private fields hide representation, protected exposes to subclasses and the package, and public methods provide behavior. Inheritance allows a subclass to reuse a parent's fields and methods; Java permits exactly one superclass but many interfaces. Polymorphism means a variable of type Shape can hold a Circle, and a call like shape.area() executes Circle's override using the runtime class's method table. Abstraction lets abstract classes and interfaces declare what an object does without committing to how. Java is not purely OOP because primitives and static members exist outside objects.

## Key points

- In Java, private fields plus public methods are the standard encapsulation mechanism, and protected means accessible within the package and subclasses.
- Java implements polymorphism through dynamic dispatch: overridden instance methods are resolved from the object's runtime class, not the reference's declared type.
- A Java class can extend only one superclass but can implement any number of interfaces; default methods can cause conflicts that must be explicitly resolved.
- Every Java class implicitly extends Object, so all objects inherit equals, hashCode, toString, getClass, and thread coordination methods like wait and notify.
- Java is not purely object-oriented because primitives (int, boolean, double) and static members can be used without any object instance.

## Your 60-second answer

Object-oriented programming in Java means designing programs as objects that combine state (fields) and behavior (methods). The four core ideas are encapsulation, inheritance, polymorphism, and abstraction. Encapsulation hides internal state behind private fields and exposes behavior through public methods, which protects invariants. Inheritance lets a class extend one superclass and inherit its fields and methods, while interfaces allow multiple type contracts. Polymorphism means a superclass or interface reference can point to a subclass object, and the JVM dispatches the overridden method based on the actual object's runtime type, not the reference type. Abstraction uses abstract classes and interfaces to define what an object does without specifying how. The trade-off is that inheritance creates tight coupling, so composition is often preferred for flexibility; Java is considered not purely OOP because primitives and statics live outside the object model.

## If they dig deeper

**When can an object reference be cast to a Java interface reference?**

An object reference can be cast to an interface type when the object's actual runtime class implements that interface. The JVM checks the cast at runtime and throws ClassCastException if the object does not implement it; upcasting to an interface is implicit, while casting back to a concrete class requires an explicit cast. This is the basis of programming to interfaces.

**What is the difference between an abstract class and an interface in Java?**

An abstract class can have instance fields, constructors, and concrete methods, so it can carry shared state and enforce a base implementation. An interface primarily declares a contract, though since Java 8 it can have default and static methods, and since Java 9 private methods. A class extends one abstract class but can implement many interfaces, so use an interface for a capability and an abstract class for shared implementation.

**Why is Java not considered a purely object-oriented language?**

Java has primitive types like int, boolean, and double that are not objects, and static variables and methods can be used without any instance. Operations on primitives and static calls are not dispatched through objects. Java intentionally kept primitives for performance and uses wrapper classes only when objects are needed.

**What methods does java.lang.Object define, and why must equals and hashCode be overridden together?**

Object defines getClass, hashCode, equals, toString, clone, and wait/notify/notifyAll; finalize was deprecated in Java 9. The contract requires equal objects to have equal hash codes, so if you override equals to compare fields, you must override hashCode consistently. Otherwise HashMap and HashSet lookups fail for equal objects that hash differently.

**How can you create an object without the new operator, and when is that appropriate?**

You can use reflection with Class.forName(...).getDeclaredConstructor().newInstance(), call clone() on a class that implements Cloneable, deserialize via ObjectInputStream, or load a class and instantiate it with a class loader. Reflection is slower and less type-safe, clone makes shallow copies unless overridden, and deserialization can bypass constructors and leave invariants uninitialized. Prefer new unless you need runtime plugin loading, copying, or persistence.

## Worked example

Consider an abstract class Shape with an abstract method area(). A Circle stores a radius and overrides area to return Math.PI * radius * radius; a Square stores a side and returns side * side. A method printArea(Shape s) prints s.area(). Calling printArea(new Circle(2)) prints 12.57 because the compiler only knows s is Shape, but at runtime the JVM looks up area in Circle's method table. Calling printArea(new Square(3)) prints 9.0 through the same call site. Adding a Triangle later requires no changes to printArea, which shows polymorphism making code open for extension without modifying existing behavior.

## Common traps

- Confusing overloading with overriding: overload resolution happens at compile time based on argument types, while overriding dispatches at runtime based on the object's class.
- Claiming Java is purely object-oriented when primitives and static members exist outside instances.
- Overriding equals without hashCode, which breaks HashMap and HashSet because equal objects must hash equally.
- Thinking Java supports multiple inheritance because it has interfaces; a class still extends only one superclass, and default method conflicts must be resolved explicitly.

</details>

---

## Isolation behaviour (`isolation-behaviour` · grid_toggle)

### 78. Triggers · Hard

*sql · gate confidence 0.7*

<sub>to object to this card: `## sql-triggers` then `match: Consider a SQL Server AFTER UPDATE trigger on a table with a`</sub>

**Question**

Consider a SQL Server AFTER UPDATE trigger on a table with a deferred unique constraint (SQL Server does not support deferrable constraints, so assume the constraint is checked immediately after the statement). The trigger updates another table. Which cells correctly describe the transaction and timing behavior?

**Options**

**Columns**: True, False
**Rows**: Trigger fires after constraint checks, Trigger runs in same transaction as UPDATE, Trigger fires once per row

**Answer (the reader is graded on)**

- Ticked: Trigger fires after constraint checks · True, Trigger runs in same transaction as UPDATE · True, Trigger fires once per row · False

**Why (right answer, wrong reason is wrong)**

→ **A. SQL Server AFTER triggers are documented to run after the DML operation and after constraints are checked, so the constraint is enforced before the trigger body executes.**
  B. SQL Server AFTER triggers run before constraint checks to allow the trigger to fix invalid data.
  C. SQL Server AFTER triggers run after constraint checks only if the constraint is deferrable, but SQL Server does not support deferrable constraints.
  D. SQL Server AFTER triggers run after constraint checks only for foreign key constraints, not for unique constraints.

**Reference answer**

The trigger runs in the same transaction as the UPDATE, so its effects commit or roll back with the statement. In SQL Server, AFTER triggers fire after the DML and after constraint checks, so the constraint is enforced before the trigger body executes. The trigger is statement-level, so it fires once per UPDATE statement, not per row.

**Graded on**

- SQL Server AFTER triggers run after constraint checks.
- The trigger executes in the same transaction as the triggering statement.
- SQL Server DML triggers are statement-level, firing once per statement.

<details><summary>The lesson this came from</summary>

A trigger is a database object bound to a table or view that automatically executes procedural SQL in response to specified DML (INSERT, UPDATE, DELETE) or DDL events. SQL Server implements DML triggers as statement-level procedures with inserted and deleted pseudo-tables; PostgreSQL supports row-level and statement-level triggers with OLD and NEW record values; MySQL implements row-level BEFORE and AFTER triggers on tables. The trigger body runs in the same transaction as the triggering statement unless the DBMS provides separate autonomous transaction features.

## Why interviewers ask this

Interviewers ask about triggers to see whether you understand how database-enforced logic differs from application logic: it runs automatically, cannot be bypassed by a client, and can hide side effects inside write paths. They probe transaction and timing semantics because a candidate who thinks all DBMSs fire AFTER triggers after constraint checks will make costly schema or recovery mistakes.

## The core idea

A trigger is a stored routine tied to an event rather than called by a client. DML changes construct transition data: SQL Server exposes inserted and deleted pseudo-tables containing the full set of affected rows for one statement; PostgreSQL and MySQL row-level triggers expose OLD and NEW values per row. The trigger executes in the same transaction as the DML, so its effects either commit or roll back with the statement unless the DBMS has autonomous transaction support. Because trigger timing relative to constraint checking differs by engine—SQL Server AFTER is post-constraint, while PostgreSQL row-level AFTER can run before deferred constraints—you must state the DBMS when discussing ordering. Recursive or long-running triggers are a common source of surprising locks and rollbacks.

## Key points

- SQL Server DML triggers are statement-level and fire once per INSERT, UPDATE, or DELETE statement, using inserted and deleted pseudo-tables for new and old row sets.
- PostgreSQL supports row-level and statement-level BEFORE, AFTER, and on views INSTEAD OF triggers; MySQL supports only row-level BEFORE and AFTER triggers on tables.
- SQL Server AFTER triggers run after the triggering DML and after constraint checks, but in PostgreSQL row-level AFTER triggers run before deferred constraint checks, and constraint timing depends on deferrability.
- In SQL Server, INSTEAD OF triggers can be defined on tables or views, while AFTER/FOR triggers cannot be defined on views.
- A trigger executes in the same transaction as the triggering statement, so an error in the trigger normally rolls back the statement, and recursive triggers can hit engine-defined nesting limits.

## Your 60-second answer

A trigger is a database object that automatically executes procedural code when a specified DML or DDL event occurs on a table or view. In SQL Server I can define an AFTER UPDATE trigger to audit salary changes; it fires once per statement and reads the inserted and deleted pseudo-tables, which hold the new and old row sets. PostgreSQL and MySQL use OLD and NEW record references in row-level triggers instead. The main benefit is enforcing logic inside the storage layer so no client can bypass it; the trade-off is that the trigger runs in the same transaction, can hide side effects, slow writes, and cause recursive cascades. I also qualify timing: SQL Server AFTER runs after constraint checks, but PostgreSQL row-level AFTER can run before deferred constraints. I use triggers only for cross-row invariants, auditing, or denormalization that constraints cannot express.

## If they dig deeper

**In SQL Server, what are the inserted and deleted tables inside a trigger?**

They are pseudo-tables available only inside DML triggers. INSERT and UPDATE populate inserted with new values; DELETE and UPDATE populate deleted with old values. Because SQL Server DML triggers fire once per statement, these pseudo-tables contain all rows affected by that statement, and you join them on the primary key to compare old and new values.

**What is the difference between AFTER and INSTEAD OF triggers in SQL Server?**

AFTER triggers execute after the DML operation has been applied and, in SQL Server, after constraints have been checked; they cannot be defined on views. INSTEAD OF triggers replace the DML operation entirely, run before any changes are made, and can be defined on tables or views, which is how views are made updatable in SQL Server.

**How do BEFORE and AFTER row-level triggers compare in PostgreSQL, and when does constraint checking happen?**

In PostgreSQL, a BEFORE row-level trigger fires before the row is written and can modify the NEW record, while an AFTER row-level trigger fires after the row is written but before the end of the statement. Non-deferred constraints are checked immediately or at statement end depending on type; deferred constraints are checked at commit. Thus a row-level AFTER trigger can see changes before a deferred constraint check rejects them.

**What problems do recursive triggers cause and how are they controlled?**

A trigger that performs the same DML on its own table can fire itself repeatedly, consuming resources and locking rows. SQL Server has a maximum nested trigger level and an option to disable recursive triggers; other DBMSs have engine-specific recursion settings. The real fix is to design trigger logic so it does not re-enter the same table, for example by using an INSTEAD OF trigger or a guard column.

**Why are triggers considered risky in high-throughput write paths?**

They add procedural work to every write inside the same transaction, can acquire locks in the trigger body, and make data changes depend on hidden code. A trigger that performs heavy queries or updates other tables serializes writes and complicates rollback analysis. Strong candidates explain that triggers are best reserved for invariants or side effects that cannot be expressed declaratively, and should be benchmarked under realistic write load.

## Worked example

Consider a SQL Server table Employees(EmployeeID, Name, Salary). A statement-level AFTER UPDATE trigger audits salary changes. An application runs UPDATE Employees SET Salary = Salary * 1.10 WHERE DepartmentID = 3, affecting two rows with old salaries 100000 and 80000. Because the trigger fires once for the whole statement, inserted holds both new salaries 110000 and 88000, while deleted holds both old salaries. The trigger body inserts into SalaryAudit by joining deleted and inserted on EmployeeID and filtering d.Salary <> i.Salary, producing two audit rows. Had the trigger body raised an error, the entire update would roll back because the trigger runs in the same transaction as the statement.

## Common traps

- Claiming AFTER triggers always fire after constraint checks: in PostgreSQL row-level AFTER triggers can run before deferred constraints, and deferrability changes when constraints are enforced.
- Writing a SQL Server trigger under the assumption it fires once per row, when DML triggers there are statement-level and inserted or deleted may contain many rows.
- Updating the same table inside an AFTER UPDATE trigger without a recursion guard, causing re-entry or hitting the engine's nested trigger limit.
- Forgetting that triggers execute inside the triggering transaction, so errors roll back both the trigger's work and the original DML statement.

</details>

---

### 79. DDL/DML/DCL/TCL · Hard

*sql · gate confidence 0.8*

<sub>to object to this card: `## sql-ddl-dml-dcl-tcl` then `match: Consider a transaction that has already executed several DML`</sub>

**Question**

Consider a transaction that has already executed several DML statements and is still open. For each statement below, indicate whether it can be rolled back by a subsequent ROLLBACK in the same transaction on PostgreSQL, Oracle, and MySQL. Assume standard behavior for each engine and that the statement is executed inside the open transaction. Select all cells where the statement is transactional (i.e., can be rolled back).

**Options**

**Columns**: PostgreSQL, Oracle, MySQL
**Rows**: CREATE TABLE, INSERT, SAVEPOINT, TRUNCATE

**Answer (the reader is graded on)**

- Ticked: CREATE TABLE · PostgreSQL, CREATE TABLE · Oracle, CREATE TABLE · MySQL, INSERT · PostgreSQL, INSERT · Oracle, INSERT · MySQL, SAVEPOINT · PostgreSQL, SAVEPOINT · Oracle, SAVEPOINT · MySQL, TRUNCATE · PostgreSQL, TRUNCATE · Oracle, TRUNCATE · MySQL

**Why (right answer, wrong reason is wrong)**

→ **A. PostgreSQL treats DDL as transactional because it logs catalog changes in the same transaction and can undo them on rollback.**
  B. PostgreSQL treats DDL as transactional because it automatically commits after each DDL statement to ensure schema changes are durable.
  C. PostgreSQL treats DDL as transactional because it does not support savepoints, so all statements are always rolled back together.
  D. PostgreSQL treats DDL as transactional because it uses a non-transactional storage engine for system catalogs.

**Reference answer**

In PostgreSQL, all listed statements are transactional and can be rolled back. In Oracle and MySQL, DDL statements (CREATE TABLE, TRUNCATE) cause implicit commits, so they cannot be rolled back by a later ROLLBACK. DML (INSERT) and TCL (SAVEPOINT) are transactional in all three engines.

**Graded on**

- PostgreSQL allows DDL inside transactions and rolls it back on ROLLBACK.
- Oracle and MySQL implicitly commit before and after DDL, so DDL cannot be rolled back.
- DML and savepoints are transactional in all three engines.

<details><summary>The lesson this came from</summary>

SQL statements are conventionally divided into four categories based on what they affect. DDL (Data Definition Language) includes CREATE, ALTER, DROP, and TRUNCATE, which define or remove schema objects such as tables, indexes, and views. DML (Data Manipulation Language) includes SELECT, INSERT, UPDATE, DELETE, and MERGE, which read or modify rows inside existing objects; some taxonomies split SELECT into a separate Data Query Language. DCL (Data Control Language) includes GRANT, REVOKE, and in SQL Server/Sybase DENY, which manage privileges. TCL (Transaction Control Language) includes COMMIT, ROLLBACK, and SAVEPOINT (SAVE TRANSACTION in SQL Server), which determine whether a multi-statement unit becomes permanent.

## Why interviewers ask this

Interviewers use this question to separate candidates who know SQL syntax from those who understand operational consequences. The real signals are whether you know which statements can be rolled back, which cause implicit commits on a given engine, and why TRUNCATE behaves like a schema change rather than a row delete. A strong answer names the categories and then immediately attaches the engine-specific transaction behavior.

## The core idea

The useful distinction is what each category changes: DDL changes the catalog or schema, DML changes row data, DCL changes authorization, and TCL changes when other work becomes durable. The categories matter because their runtime behavior differs: DDL acts on metadata, may implicitly commit, and does not accept a WHERE clause, while DML can participate in an explicit transaction. In Oracle and MySQL DDL usually causes implicit commits; PostgreSQL allows many DDL statements inside transactions. Misclassifying TRUNCATE as DML therefore leads to wrong assumptions about rollback, filtering, and identity reset behavior.

## Key points

- DDL includes CREATE, ALTER, DROP, and TRUNCATE; these change schema objects, and in Oracle and MySQL they usually cause implicit commits.
- DML includes SELECT, INSERT, UPDATE, DELETE, and MERGE; it reads or modifies row data and stays within an open transaction in engines that support transactional DML.
- DCL includes GRANT and REVOKE; DENY is a SQL Server/Sybase extension, not part of standard SQL.
- TCL includes COMMIT, ROLLBACK, and SAVEPOINT (SAVE TRANSACTION in SQL Server); rolling back to a savepoint undoes only later work and does not end the outer transaction.
- TRUNCATE is DDL rather than DML: it removes all rows, does not accept a WHERE clause, and its rollback and reset behavior differs from DELETE by engine.

## Your 60-second answer

SQL is split into four groups by effect. DDL — CREATE, ALTER, DROP, TRUNCATE — changes the schema: tables, indexes, views. DML — INSERT, UPDATE, DELETE, and often SELECT — reads or changes rows inside existing objects. DCL — GRANT, REVOKE, and in SQL Server DENY — controls permissions. TCL — COMMIT, ROLLBACK, and SAVEPOINT — controls whether a group of statements becomes permanent. The practical distinction is rollback behavior: DML runs inside transactions, while DDL often implicitly commits in Oracle and MySQL, though PostgreSQL allows more transactional DDL. TRUNCATE removes all rows but is DDL, so its logging and rollback behavior differ from DELETE. That distinction is usually what the interviewer is checking.

## If they dig deeper

**Is SELECT a DML command or a separate category?**

Most working summaries group SELECT with DML because it manipulates data, but a stricter taxonomy separates reads into DQL (Data Query Language). In an interview, say it is often included under DML; the important point is that SELECT does not modify data and usually participates in the same transaction model as other DML.

**Why is TRUNCATE considered DDL instead of DML?**

TRUNCATE acts on the table as a whole rather than on individual rows; it has no WHERE clause and often resets identity values. Because it is DDL, engines like Oracle and MySQL may treat it as an implicit-commit operation, whereas DELETE is transactional DML and can filter rows.

**What happens to an active transaction when you run a DDL statement in Oracle versus PostgreSQL?**

In Oracle, DDL issues an implicit commit before and after the statement, so prior work cannot be rolled back afterward. In PostgreSQL, CREATE, ALTER, DROP, and TRUNCATE can run inside a transaction block and be rolled back normally. MySQL also causes implicit commits for most DDL.

**How does a savepoint differ from COMMIT or ROLLBACK?**

COMMIT makes the entire transaction durable, and ROLLBACK undoes the whole transaction. A savepoint marks a point inside the transaction; ROLLBACK TO SAVEPOINT, or ROLLBACK TRANSACTION savepoint_name in SQL Server, undoes only later statements and leaves the outer transaction open, so you still must COMMIT or ROLLBACK the whole unit.

**Can you combine DDL, DML, DCL, and TCL into one transaction in a portable way?**

Not portably. DML and TCL work together in all transactional engines, but DDL and DCL transaction behavior varies sharply: PostgreSQL generally supports transactional DDL, Oracle and MySQL often commit implicitly, and SQL Server supports many but not all DDL operations transactionally. You need to check the engine's rules before relying on rollback of schema or permission changes.

## Worked example

In SQL Server, a warehouse application first creates an inventory table with DDL: `CREATE TABLE Inventory (id INT PRIMARY KEY, qty INT NOT NULL);`. DCL gives the app access: `GRANT SELECT, UPDATE ON Inventory TO warehouse_app;`. A transaction then inserts and later updates a row using DML: `BEGIN TRANSACTION; INSERT INTO Inventory (id, qty) VALUES (1, 100); SAVE TRANSACTION after_insert; UPDATE Inventory SET qty = 90 WHERE id = 1;`. Rolling back to the savepoint with `ROLLBACK TRANSACTION after_insert;` undoes the UPDATE but keeps the INSERT; a final `COMMIT;` makes the inserted row durable. This separates schema creation, permission, row changes, and transaction control to show why each category exists.

## Common traps

- Listing TRUNCATE as DML because it deletes data; it is DDL, has no WHERE clause, and may implicitly commit, so its failure behavior is very different from DELETE.
- Claiming all DDL can never be rolled back; PostgreSQL allows many DDL statements inside transactions, while Oracle and MySQL usually do not.
- Presenting DENY as standard SQL DCL; DENY is a SQL Server/Sybase extension, and standard SQL defines GRANT and REVOKE.
- Ignoring that SELECT is often separated as DQL in stricter taxonomies; if you insist it is DML without noting the split, you can look unaware of the common classification debate.

</details>

---

## Method semantics (`method-semantics` · grid_toggle)

### 80. Service Discovery · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-service-discovery` then `match: Which combinations of discovery mode and registration method`</sub>

**Question**

Which combinations of discovery mode and registration method are valid in service discovery? Select all cells that hold.

**Options**

**Columns**: Self-registration, Third-party registration
**Rows**: Client-side discovery, Server-side discovery

**Answer (the reader is graded on)**

- Ticked: Client-side discovery · Self-registration, Client-side discovery · Third-party registration, Server-side discovery · Self-registration, Server-side discovery · Third-party registration

**Reference answer**

Client-side discovery can use either self-registration or third-party registration; the client queries the registry and calls an instance directly. Server-side discovery also supports both registration methods; a load balancer queries the registry and routes to an instance. The discovery mode and registration method are orthogonal.

**Graded on**

- Client-side discovery: client queries registry and selects instance.
- Server-side discovery: load balancer queries registry and routes.
- Self-registration: instance registers itself and sends heartbeats.
- Third-party registration: external controller updates registry.

<details><summary>The lesson this came from</summary>

Service discovery is the component that lets a client find a live instance of a named service without hardcoded host:port pairs. Instances register with a service registry—Consul, etcd, ZooKeeper, or an orchestration API—and the registry keeps a mapping from service name to current network locations. Discovery can happen client-side, where the client queries the registry and selects an instance, or server-side, where a load balancer queries the registry and routes. Health tracking removes unreachable instances before they receive traffic.

## Why interviewers ask this

In microservices, instances scale, fail, and move; static endpoint configuration breaks under those conditions. Interviewers use service discovery to test whether you can route traffic to ephemeral instances and reason about the health and consistency paths during failure. Large system design problems often assume dynamic service locations, so a weak discovery story undermines the rest of the design.

## The core idea

Service discovery separates the identity of a service from the network location of its instances. A highly available registry stores the mapping from service name to a set of live endpoints; instances register themselves or are registered by an external controller. Health state is maintained either by leases or heartbeats from the instance, or by active checks from the registry. Clients either query the registry directly and load-balance, or delegate routing to a server-side load balancer. The hard part is consistency: a registry can only reflect change as fast as heartbeats, lease expiry, or active checks allow, so there is always a propagation delay after failure.

## Key points

- Client-side discovery has the client query the registry and then call an instance directly; server-side discovery puts a load balancer between clients and instances.
- A service registry must be highly available and up-to-date; common implementations include Consul, etcd, and ZooKeeper.
- Self-registration lets instances register and deregister themselves and send heartbeats; third-party registration uses an external controller or orchestration event to update the registry.
- etcd does not actively poll HTTP health endpoints; it deletes keys when a client-managed lease expires. Consul can perform active health checks.
- There is always a lag between an instance failing and every client stopping traffic to it, bounded by heartbeat or lease TTL plus client cache refresh.

## Your 60-second answer

Service discovery is how a service finds the current network location of another service instance without hardcoded addresses. Each instance registers in a service registry—Consul, etcd, or ZooKeeper—which stores the mapping from service name to live host:port endpoints, and removes entries when instances fail health checks or miss heartbeats. In client-side discovery, the caller queries the registry and selects an instance; in server-side discovery, a load balancer queries the registry and routes the request. Registration can be self-registration by the instance or third-party registration by an orchestrator. The main trade-off is freshness versus availability: a registry can only reflect failure as fast as its TTL or check interval, so clients may briefly call an instance that is already down unless they retry or fall back.

## If they dig deeper

**What is the difference between client-side and server-side discovery?**

In client-side discovery, the client queries the registry, obtains the list of instances, and performs load balancing itself before calling the instance directly. In server-side discovery, the client sends the request to a load balancer or router, which queries the registry and forwards traffic to a chosen instance. Client-side discovery gives clients more control and removes a network hop, but requires a discovery client and load-balancing logic in every service.

**How do instances register themselves, and what are the alternatives?**

Self-registration means the instance calls the registry on startup, deregisters on shutdown, and may send heartbeats. Third-party registration uses an external controller or orchestration platform, such as Kubernetes, to detect containers and update the registry. Self-registration couples the service to the registry; third-party registration centralizes lifecycle awareness but can miss an unhealthy process if the container still exists.

**How does the registry know if an instance is still healthy?**

It depends on the registry. Consul can run active health checks, such as HTTP probes, and mark instances unhealthy after repeated failures. etcd uses client-managed leases: the instance must refresh its lease with keep-alives before TTL expiry, otherwise the key is deleted. ZooKeeper uses ephemeral znodes tied to a session heartbeat. Active checks can test external dependencies; lease expiration only proves the client process can still reach the registry.

**What happens if the service registry itself goes down?**

A strong answer distinguishes the control plane from the data plane. Existing clients may keep using cached endpoints, and server-side load balancers may keep routing from their last known table, so traffic can continue temporarily. New instances cannot register and old ones cannot deregister until the registry recovers, so changes are frozen and failures may not be removed. For this reason the registry is typically run as a small replicated highly available cluster and treated as critical infrastructure.

**How do you avoid a thundering herd of clients querying the registry on every request?**

Clients cache the endpoint list and subscribe to updates or refresh lazily with a bounded TTL or jitter. In server-side discovery, only the load balancer queries the registry, so client fan-out is much smaller. Service meshes push endpoint updates to sidecar proxies through the control plane, avoiding repeated polling. The tradeoff is cache staleness: after a failure, some requests may still target the dead instance until refresh.

## Worked example

Consider a payments service with three instances, each registered under the same service name and sending keep-alives every 3 seconds. The registry lease has a TTL of 10 seconds. A client caches the endpoint list for 30 seconds and load-balances across the instances. If instance B crashes at t=0 and its last keep-alive was at t=0, the registry deletes it when the lease expires at about t=10; before that, the registry still lists B. If the client last refreshed at t=-5, it will keep a cached list containing B until t=25, so it can still call the dead instance. That window is why client-side discovery needs retries or a fallback path, while server-side load balancers can perform active health checks and remove B sooner.

## Common traps

- Assuming every registry actively health-checks instances: etcd uses leases, while Consul supports active HTTP and TCP checks.
- Hardcoding service endpoints in configuration and calling that service discovery: it breaks when instances scale or move.
- Confusing the registry with the load balancer: in client-side discovery, clients query the registry but still call instances directly.
- Forgetting cache staleness: a client with cached endpoints can keep sending traffic to a dead instance after the registry removes it.

</details>

---

### 81. Design a news feed · Medium

*system_design · gate confidence 0.8*

<sub>to object to this card: `## sd-design-a-news-feed` then `match: A news feed system uses a hybrid fanout model. For each scen`</sub>

**Question**

A news feed system uses a hybrid fanout model. For each scenario, decide whether the system should use push-based fanout (write to follower timelines at post time), pull-based fanout (merge at read time), or a hybrid approach (push to some followers, pull for others). Assume standard implementations: push means appending the post ID to each follower's timeline cache at write time; pull means fetching the followed account's recent posts at read time. Select all cells that correctly match the scenario to the fanout strategy.

**Options**

**Columns**: Push, Pull, Hybrid
**Rows**: User with 300 followers, Celebrity with 50M followers, User with 10,000 followers

**Answer (the reader is graded on)**

- Ticked: User with 300 followers · Push, Celebrity with 50M followers · Pull, User with 10,000 followers · Hybrid

**Reference answer**

Correct cells: (0,0), (1,1), (2,2). A user with 300 followers gets push fanout because the write amplification is bounded and reads become fast. A celebrity with 50M followers gets pull fanout to avoid millions of timeline writes per post. A user with 10,000 followers gets a hybrid: push to recently active followers and pull for the rest, balancing read latency and write cost.

**Graded on**

- Push fanout is used for ordinary users with up to a few thousand followers.
- Pull fanout is used for celebrities with millions of followers to avoid write amplification.
- Hybrid fanout pushes to a subset of recently active followers and pulls for the rest.

<details><summary>The lesson this came from</summary>

A news feed system aggregates content created by accounts a user follows, ranks the content, and serves it as a paginated list. The write path stores new posts and distributes them to follower timelines; the read path assembles a feed from stored or pulled candidate posts. Core components include post storage, user graph storage, feed generation, ranking, caching, and media delivery via CDN.

## Why interviewers ask this

Interviewers ask this to test whether you can handle a read-heavy, fanout-heavy system with huge variance in follower counts. They probe your ability to choose between push and pull models, design caching, model data, and explain trade-offs between latency, consistency, and write amplification. This question is known from Facebook/Meta and Instagram design loops.

## The core idea

A news feed is a read-heavy system: reads outnumber writes by roughly 100:1 in typical designs. For ordinary users, fanout on write (push) precomputes follower timelines so reads are fast; for celebrities, fanout on read (pull) avoids writing to millions of timelines. Ranking is not just reverse chronological—it scores candidates by recency, affinity, and engagement. Caching and precomputation absorb most read load, while asynchronous fanout and partitioning absorb write load. The central trade-off is read latency vs write amplification and freshness.

## Key points

- For ordinary users with up to a few thousand followers, push-based fanout writes each new post to the follower timelines at post time, making feed reads O(1) or simple cache lookups.
- For accounts with millions of followers, pull-based fanout avoids massive write amplification; their posts are merged into follower feeds at read time instead of written to each timeline.
- Feed ranking uses candidate generation from followed accounts, then scoring by factors like recency, affinity, engagement, and content type, not just chronology.
- Reads dominate: typical designs assume a 100:1 read-to-write ratio; caching hot feeds in Redis/Memcached with LRU and serving media via CDN reduces database and origin load.
- Data is sharded by user ID or post ID, with asynchronous fanout queues and batch writes to handle spikes and eventual consistency across follower timelines.

## Your 60-second answer

A news feed system needs to store posts and serve each user a personalized, ranked list of content from accounts they follow. The core decision is fanout. For ordinary users, I'd push each new post to the follower timelines at write time: the post ID is appended to a cached list for each follower, so reads are fast. For celebrities with millions of followers, I'd not fan out on write; instead, I'd pull their recent posts at read time and merge them into the follower's feed. I'd rank the candidate posts using a scoring model based on recency, affinity, engagement, and content type, then return the top few hundred. Reads are cached with LRU and CDNs; writes are processed asynchronously through queues and batched. The main trade-off is latency versus consistency: push gives low-latency reads but eventual consistency during fanout.

## If they dig deeper

**How will you handle fanout: push model, pull model, or hybrid?**

Use a hybrid. For normal users with up to a few thousand followers, push the post to each follower's timeline storage or cache at write time, because read latency is more important and the fanout cost is bounded. For accounts with millions of followers, do not push; instead pull their recent posts at read time and merge them into the feed, avoiding write amplification. Optionally push to recently active followers and let inactive followers pull on next login.

**How does the system change for a user with millions of friends/followers?**

For a celebrity, pushing one post to all followers would generate millions of timeline writes, so the write path must be changed. Store celebrity posts in a separate timeline or post list and merge them at read time for each follower. If we want lower read latency for active users, we can maintain a hybrid: push to a subset of recently active followers and have the rest pull, possibly with a cap on fanout size.

**How will you fetch and score new content at scale - especially when a user opens the app after days?**

The read service generates the feed lazily on first open: it pulls recent posts from each followed account or from the user's precomputed timeline cache, merges them, and passes candidates to a ranker. For a dormant user, there is no continuously updated timeline; we compute the feed on demand and cache the result for a short time. Ranking must consider recency and user affinity so older posts from close friends can still appear above newer, less relevant posts, rather than a strict reverse-chronological order.

**How will you handle the scalability of writes and reads - e.g., batching, caching, partitioning?**

Writes go through an asynchronous fanout service that batches timeline inserts and partitions work by user ID or shard; this smooths spikes when a popular user posts. Reads are served from distributed caches like Redis or Memcached with LRU eviction, backed by read replicas of the database. Media is offloaded to object storage and served via CDN, so the feed service only handles metadata. Pagination limits response size and reduces load.

## Worked example

Assume a system with 500M daily active users, 95M photo posts and 5M video posts per day, and a 100:1 read-to-write ratio. For write fanout: if a normal user with 300 followers posts one photo, the fanout service must insert that post ID into 300 follower timeline caches. If the system handles 500 post writes per second, that is 150,000 timeline writes per second, which can be done by batching inserts across shards. For a celebrity with 50M followers, the same fanout would require 50M timeline inserts per post, so the system does not push; it stores the post once and, at read time, merges the celebrity's recent posts into each follower's feed. A returning user who follows 500 accounts triggers a read that fetches recent post IDs from those accounts, ranks them by recency and affinity, and returns the top 200. With 50,000 feed requests per second, caching precomputed feeds for active users in Redis and serving media from a CDN can reduce database reads by an order of magnitude.

## Common traps

- Proposing only push-based fanout for all users; with celebrity accounts this causes massive write amplification and can delay post visibility for hours.
- Designing the feed as strictly reverse chronological; real news feeds rank by relevance, so ignoring ranking and personalization misses a core requirement.
- Jumping to a final architecture without estimating read/write volume or identifying bottlenecks; interviewers expect iterative scaling based on load.
- Storing media in the same relational database as post metadata; images and videos must go to object storage and CDN, not bloat the primary database.

</details>

---

## Cards the gate rejected

Judge whether it was right. Each was thrown away.

- **advanced-graphs** (assemble): Assemble the line of code that correctly implements the key step of Kahn's algorithm for topological sorting. The line should process the next node with zero indegree and add it to the result. Assume `queue` is a deque of nodes with indegree 0, `indegree` is a list of indegrees, `graph` is an adjacency list, and `result` is a list. The line should be:
```
node = queue.popleft()
result.append(node)
for neighbor in graph[node]:
    indegree[neighbor] -= 1
    if indegree[neighbor] == 0:
        queue.append(neighbor)
```
But only the line `node = queue.popleft()` is missing. Assemble that line from the tokens.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **backtracking** (order): Arrange the following steps in the correct order for a backtracking algorithm that generates all combinations of a set of distinct integers, where each combination is a subset of the input. Assume the algorithm uses a mutable list `path` to build the current combination and a result list to collect all valid combinations. The steps are shuffled.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **backtracking** (match): Match each backtracking problem to its worst-case time complexity, assuming the standard backtracking solution described in the lesson and no additional pruning beyond what is typical for that problem. For Word Search, assume board dimensions m x n and word length L. For N-Queens, assume n queens on an n x n board.
  - Gate said: refers to unseen material: 'the lesson'

- **backtracking** (assemble): Assemble the line that undoes the last choice in a backtracking recursive function, so the mutable candidate is restored before returning to the caller. The line is a single statement in Python.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **backtracking** (match): Match each backtracking operation with its typical time complexity. Assume standard implementations and worst-case analysis.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **binary-search** (order): Arrange the following steps in the correct order to perform a binary search for a target in a sorted array using a closed interval [low, high].
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **binary-search** (match): Match each binary search variant to its worst-case time complexity, assuming the standard implementation described in the lesson and distinct values where applicable.
  - Gate said: refers to unseen material: 'the lesson'

- **binary-search** (assemble): Assemble the line that computes the middle index in a binary search loop, avoiding integer overflow. Use the tokens provided.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-acid-properties** (order): Arrange the following steps in the order they occur when a database transaction commits with write-ahead logging, from first to last.
  - Gate said: not answerable: The question does not provide the steps to arrange.

- **cs-acid-properties** (order): Order the steps a database engine takes to guarantee durability when a transaction commits, from first to last.
  - Gate said: not answerable: The question does not provide the steps to arrange.

- **cs-acid-properties** (match): Match each ACID property to the failure it primarily protects against.
  - Gate said: not answerable: The question does not provide the items to match.

- **cs-acid-properties** (order): Order the steps a database engine takes to guarantee ACID properties during a transaction that commits successfully, from the start of the transaction to the acknowledgment of the commit.
  - Gate said: not answerable: The question does not provide the steps to arrange.

- **cs-acid-properties** (claim_grid): A database transaction is running under serializable isolation with synchronous durability. For each statement, mark whether it is guaranteed to hold.
  - Gate said: not answerable: The question does not provide the statements to mark.

- **cs-acid-properties** (assemble): Assemble the definition of Atomicity in ACID by arranging the tokens in the correct order.
  - Gate said: not answerable: The question does not provide the tokens to arrange.

- **cs-acid-properties** (claim_grid): Which of the following statements about ACID properties are true? Mark each statement as true or false.
  - Gate said: not answerable: The question does not provide the statements to mark.

- **cs-acid-properties** (order): Arrange the following steps in the order a database engine performs them to guarantee ACID properties when a transaction commits:
  - Gate said: not answerable: The question does not provide the steps to arrange.

- **cs-acid-properties** (match): Match each ACID property to the failure mode it primarily protects against.
  - Gate said: not answerable: The question does not provide the items to match.

- **cs-acid-properties** (bucket): Classify each scenario by the ACID property it primarily guarantees.
  - Gate said: not answerable: The question does not provide the scenarios to classify.

- **cs-cpu-scheduling** (match): Match each CPU scheduling term with its definition. Assume standard definitions from an operating systems course.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-cpu-scheduling** (assemble): Assemble the definition of CPU scheduling by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-cpu-scheduling** (pick_one): Three jobs arrive at time 0 with CPU bursts: A=24 ms, B=3 ms, C=3 ms. Which scheduling policy gives the lowest average turnaround time for this batch, assuming all runtimes are known and no preemption?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'FCFS'

- **cs-cpu-scheduling** (order): Three jobs arrive at time 0 with CPU bursts: A=24 ms, B=3 ms, C=3 ms. The scheduler uses non-preemptive SJF. Order the jobs by the time each first gets the CPU, from earliest to latest.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-cpu-scheduling** (match): Match each CPU scheduling policy to the primary problem it is known for.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-deadlocks** (pick_one): A system has two resource types, each with a single instance. Process P1 holds resource R1 and requests R2. Process P2 holds R2 and requests R1. No preemption is possible. Which statement is true?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-deadlocks** (match): Match each deadlock handling strategy to its primary characteristic.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-deadlocks** (assemble): Assemble the definition of a deadlock by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-dns** (pick_one): A recursive resolver receives an NXDOMAIN response for a missing name. The SOA record in the authority section has a TTL of 900 seconds and a MINTTL field of 300 seconds. How long may the resolver cache the negative answer?
  - Gate said: guessable by shape: an option is far longer than the rest: '0 seconds (negative answers are never cached)'

- **cs-dns** (pick_one): A recursive resolver receives a query for a name that does not exist and gets an NXDOMAIN response from the authoritative server. The SOA record in the authority section has a TTL of 900 seconds and a MINTTL field of 300 seconds. How long may the resolver cache this negative response?
  - Gate said: guessable by shape: an option is far longer than the rest: '0 seconds (negative responses are never cached)'

- **cs-dns** (assemble): Assemble the definition of DNS by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-dns** (match): Match each DNS term on the left with its correct meaning on the right.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-inter-process-communication** (pick_one): A parent process creates an anonymous pipe, forks a child, and both processes close the appropriate ends so the parent reads and the child writes. The child writes 10 bytes and exits without closing its write descriptor explicitly. What does the parent's read() return after the child exits?
  - Gate said: guessable by shape: an option is far shorter than the rest: '10'

- **cs-inter-process-communication** (match): Match each IPC mechanism to its primary failure mode or limitation.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-object-oriented-programming-principles** (match): Match each OOP principle to the problem it primarily addresses.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-page-replacement-algorithms** (match): Match each page replacement algorithm with its defining eviction criterion.
  - Gate said: not answerable: The algorithms and criteria to match are missing.

- **cs-page-replacement-algorithms** (match): Match each page replacement algorithm with the error or anomaly it is most directly associated with.
  - Gate said: not answerable: The items to match are missing.

- **cs-page-replacement-algorithms** (claim_grid): Consider the following statements about page replacement algorithms. Mark each statement as true or false. Assume a standard implementation and a fixed reference string.
  - Gate said: not answerable: The statements to be marked are missing.

- **cs-page-replacement-algorithms** (bucket): Classify each page replacement algorithm by whether it can exhibit Belady's anomaly (more frames can cause more faults for the same reference string).
  - Gate said: not answerable: The algorithms to classify are missing.

- **cs-page-replacement-algorithms** (claim_grid): For each statement about page replacement algorithms, mark it as true or false.
  - Gate said: not answerable: The statements to be marked are missing.

- **cs-race-conditions** (pick_one): A shared counter starts at 0. Two threads each execute counter = counter + 1 exactly once, with no synchronization. Which final value is possible?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-race-conditions** (pick_one): A shared counter starts at 0. Thread A executes counter = counter + 1, and Thread B executes counter = counter + 1. Both threads run once. Without synchronization, what is the final value of the counter?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-race-conditions** (pick_one): A shared counter is protected by a mutex. Thread A acquires the mutex, reads the counter value 5, and is then descheduled before writing the incremented value. Thread B acquires the mutex, reads the counter value 5, increments it to 6, writes 6, and releases the mutex. Thread A resumes, increments its stale read to 6, writes 6, and releases the mutex. What is the final counter value?
  - Gate said: guessable by shape: an option is far longer than the rest: 'The result is nondeterministic because the mutex does not prevent lost updates.'

- **cs-race-conditions** (assemble): Assemble the definition of a race condition from the tokens below.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-socket-programming** (order): Arrange the following steps in the correct order for a TCP server to accept a client connection and exchange data, assuming the socket is already created. The server must be able to accept connections and then communicate with the client.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-socket-programming** (order): Arrange the following steps in the correct order for a TCP server to accept a client connection and exchange data, assuming a standard blocking implementation.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-tcp-3-way-handshake** (order): Arrange the following steps in the correct order for a standard TCP three-way handshake, assuming no payload data is sent and no options are negotiated.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-tcp-3-way-handshake** (assemble): Assemble the definition of the TCP three-way handshake from the tokens below.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-tcp-3-way-handshake** (order): Arrange the following events in the order they occur during a standard TCP three-way handshake, from first to last.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-tcp-3-way-handshake** (order): Arrange the following steps of the TCP three-way handshake in the order they occur, from first to last. Assume a standard handshake with no data carried in any segment.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-tcp-3-way-handshake** (order): Arrange the following steps of the TCP three-way handshake in the order they occur, from first to last. Assume a standard handshake with no data in the SYN or final ACK.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-tlb-and-caching** (assemble): Assemble the definition of a translation lookaside buffer (TLB) from the tokens below.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-tlb-and-caching** (match): Match each cache/TLB event with its cause.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-tls-ssl-handshake** (assemble): Assemble the definition of the TLS handshake by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **graphs** (order): Arrange the following steps in the correct order to perform Kahn's algorithm for topological sorting on a directed acyclic graph. Assume the graph is stored as an adjacency list and you have an array of indegrees for all vertices.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **graphs** (assemble): Assemble the line of code that initializes the visited set for a graph traversal, given that the graph has V vertices. Use the tokens provided.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **graphs** (match): Match each graph operation with its time complexity on an adjacency-list graph with V vertices and E edges, assuming standard implementations and no extra constraints.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **graphs** (pick_one): You are given a directed graph with n nodes and m edges, where each edge has a positive weight. You need to find the shortest path from a single source to all other nodes. Which algorithm should you use?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'BFS'

- **graphs** (pick_one): Which of the following is a valid counter-example showing that BFS does not always find the shortest path in a graph with weighted edges?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **heap-priority-queue** (match): Match each heap-based operation to its worst-case time complexity for a binary heap containing n elements. Assume a standard array-based binary heap implementation.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-abstract-class-vs-interface** (tap_in_place): Which line contains the bug? Assume Java 17.
  - Gate said: not answerable: No code snippet is provided, so the candidate cannot identify a line.

- **java-abstract-class-vs-interface** (assemble): Assemble the definition of an abstract class in Java by arranging the tokens in the correct order. The definition should state that an abstract class is a class that cannot be instantiated and can declare both abstract and concrete methods.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-checked-vs-unchecked-exceptions** (assemble): Assemble the definition of a checked exception in Java by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-checked-vs-unchecked-exceptions** (tap_in_place): Which line contains the bug? The code is intended to compile and run without forcing callers to handle a programming error.
  - Gate said: not answerable: The question references a code snippet that is not provided, so the candidate cannot see the lines to identify the bug.

- **java-checked-vs-unchecked-exceptions** (assemble): Assemble the method signature that correctly declares that this method may throw a checked exception, using the tokens below.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-checked-vs-unchecked-exceptions** (tap_in_place): Which line will cause a compile-time error?
  - Gate said: not answerable: The question references a code snippet that is not provided, so the candidate cannot see the lines to identify the error.

- **java-checked-vs-unchecked-exceptions** (match): Match each exception-related scenario to the correct compile-time or runtime behavior. Assume standard Java compilation and execution.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-checked-vs-unchecked-exceptions** (grid_toggle): Classify each exception type by whether it is checked or unchecked in Java. Select all cells that are correct.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-checked-vs-unchecked-exceptions** (assemble): Assemble the method signature that correctly declares that this method may throw a checked exception, using the tokens below. The method is named `readFile` and takes a `String path` parameter.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-collections-framework** (assemble): Assemble the definition of the Java Collections Framework by placing the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-collections-framework** (assemble): Assemble the method signature for adding an element to a List in Java. Use all tokens exactly once.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-collections-framework** (pick_one): You have a PriorityQueue<Integer> initialized with the following elements added in this order: 5, 1, 3. What does peek() return?
  - Gate said: guessable by shape: an option is far longer than the rest: 'The result is unspecified'

- **java-collections-framework** (assemble): Assemble the line that declares a list of strings using the List interface and the ArrayList implementation.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-collections-framework** (match): Match each Java Collections Framework mistake with the consequence it causes.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-comparable-vs-comparator** (assemble): Assemble the method signature of the Comparator interface's single abstract method, using the tokens below. The signature should be exactly as defined in java.util.Comparator<T>.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-comparable-vs-comparator** (assemble): Assemble the definition of the Comparable interface's method by placing the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-comparable-vs-comparator** (pick_one): Given the following code, what is the output?

```java
import java.util.*;

class Employee implements Comparable<Employee> {
    String name;
    int age;
    Employee(String name, int age) { this.name = name; this.age = age; }
    public int compareTo(Employee other) { return Integer.compare(this.age, other.age); }
    public String toString() { return name + ":" + age; }
}

public class Main {
    public static void main(String[] args) {
        List<Employee> list = Arrays.asList(
            new Employee("Alice", 30),
            new Employee("Bob", 25),
            new Employee("Charlie", 35)
        );
        Collections.sort(list);
        System.out.println(list);
    }
}
```
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-concurrency** (assemble): Assemble the method signature for atomically incrementing an AtomicInteger and returning the new value.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-concurrency** (pick_one): Two threads each increment a shared int counter 1000 times using counter++. What is the maximum possible final value of the counter?
  - Gate said: guessable by shape: an option is far longer than the rest: 'It is unpredictable and can exceed 2000'

- **java-concurrency** (assemble): Assemble the definition of a happens-before relationship in the Java Memory Model by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-concurrency** (assemble): Assemble the line that atomically increments a shared counter using java.util.concurrent.atomic.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-concurrenthashmap** (assemble): Assemble the line that creates a thread-safe map that rejects null keys and values, using the standard Java 8+ implementation.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-default-and-static-interface-methods** (assemble): Assemble the line that declares a default method in a Java interface, using the tokens below. The method is named greet, takes no parameters, returns a String, and its body returns the string "Hello".
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-equals-and-hashcode-contract** (match): Match each operation to its complexity in a standard Java HashMap implementation, assuming a good hash function and no pathological collisions.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-equals-and-hashcode-contract** (assemble): Assemble the equals/hashCode contract as stated in the java.lang.Object API. Arrange the tokens to form the correct sentence.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-equals-and-hashcode-contract** (assemble): Assemble the method signature for the equals method that correctly overrides Object.equals, as required by the equals/hashCode contract.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-equals-and-hashcode-contract** (pick_one): Consider a Student class that overrides equals to compare id and name but does not override hashCode. Two distinct Student objects a and b have the same id and name, so a.equals(b) is true. A HashSet<Student> set is created, and set.add(a) is called. What is the result of set.contains(b)?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'true'

- **java-executor-framework** (assemble): Assemble the signature of the ExecutorService method that submits a Callable task and returns a Future representing its pending result. Use all tokens.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-hashset-vs-treeset** (match): Match each term to its correct meaning. Assume standard Java implementations and natural ordering unless stated otherwise.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-hashset-vs-treeset** (assemble): Assemble the line that creates a TreeSet with natural ordering.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-hashset-vs-treeset** (pick_one): Consider a TreeSet<BigDecimal> using natural ordering. You add new BigDecimal("1.0") and then new BigDecimal("1.00"). What is the size of the set after both additions?
  - Gate said: guessable by shape: an option is far longer than the rest: 'It throws ClassCastException'

- **java-hashset-vs-treeset** (assemble): Assemble the method signature for adding an element to a HashSet, using the tokens below. The signature should be the standard Set interface method that returns a boolean indicating whether the set changed.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-immutability** (match): Match each operation on an immutable class to its complexity, assuming standard implementations and no extra memory beyond the object itself.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-java-memory-model** (assemble): Assemble the line that declares a volatile boolean field named done in a Java class.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-java-memory-model** (pick_one): Consider the following Java code:

```java
class Example {
    int value = 0;
    volatile boolean done = false;

    void writer() {
        value = 42;
        done = true;
    }

    void reader() {
        while (!done) {}
        System.out.println(value);
    }
}
```

Thread A calls `writer()`, and Thread B calls `reader()`. What is the guaranteed output?
  - Gate said: guessable by shape: an option is far shorter than the rest: '42'

- **java-jdbc** (match): Match each JDBC error cause to the mistake that produces it.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-jvm-and-memory** (assemble): Assemble the definition of a GC root in the HotSpot JVM by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-jvm-architecture** (pick_one): A Java application runs on HotSpot. A method creates an object with `new`, and the object's reference never leaves the method or the thread. Under standard HotSpot optimizations, where can the object's fields be stored?
  - Gate said: guessable by shape: one option is the only one carrying code: 'Only on the heap, because all objects created with `new` must be heap-allocated.'

- **java-jvm-architecture** (match): Match each JVM runtime data area with the error or issue most directly associated with it.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-lambda-expressions** (pick_one): Given the following code, what is the output?

```java
import java.util.function.Function;

public class Test {
    public static void main(String[] args) {
        Function<Integer, Integer> f = x -> x * 2;
        System.out.println(f.apply(5));
    }
}
```
  - Gate said: guessable by shape: an option is far longer than the rest: 'Compilation error'

- **java-lambda-expressions** (assemble): Assemble the definition of a lambda expression in Java by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-lambda-expressions** (assemble): Assemble a valid Java lambda expression that implements Runnable and prints "Hello" to standard output. Use the tokens provided.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-lock-interface-and-reentrantlock** (match): Match each ReentrantLock usage error with its consequence. Assume the lock is uncontended at the time of the erroneous call.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-memory-leaks** (match): Match each Java memory-leak scenario with the GC root that keeps the leaked objects reachable. Assume standard Java semantics and that no cleanup code runs.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-memory-leaks** (grid_toggle): Consider a Java application with a memory leak. For each combination of scenario and statement, indicate whether the statement is true for that scenario. Assume standard JVM behavior and no explicit cleanup unless stated.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-oop-concepts** (pick_one): In Java, which access modifier restricts a field so that it can be accessed only within the same class?
  - Gate said: guessable by shape: an option is far longer than the rest: 'package-private (no modifier)'

- **java-oop-concepts** (assemble): Assemble the Java method signature that overrides Object's equals method correctly, using all tokens.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-polymorphism** (pick_one): Consider the following Java code:

class Animal {
    void speak() { System.out.println("Animal speaks"); }
}

class Dog extends Animal {
    void speak() { System.out.println("Woof"); }
    void speak(int times) { for (int i = 0; i < times; i++) System.out.println("Woof"); }
}

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        a.speak();
    }
}

What is the output?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'Woof'

- **java-streams-api** (grid_toggle): Consider the following operations in the Java Stream API. For each operation, indicate whether it is an intermediate operation (returns a Stream and is lazy) or a terminal operation (triggers processing and returns a non-stream result or side effect). Assume standard Java 8+ behavior.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-streams-api** (match): Match each Streams API term with its correct meaning.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-streams-api** (pick_one): Given the following code, what is the output?

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .collect(Collectors.toList());
System.out.println(result);
```
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-streams-api** (tap_in_place): Consider the following Java code that uses the Stream API:

```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
Stream<String> stream = names.stream();
stream.forEach(System.out::println);
stream.forEach(System.out::println);
```

Which line causes an IllegalStateException when executed?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-streams-api** (pick_one): Consider the following code:

List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> result = numbers.parallelStream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .collect(Collectors.toList());

What is the guaranteed output of this code?
  - Gate said: guessable by shape: an option is far longer than the rest: 'The output is unpredictable because the stream is parallel.'

- **java-streams-api** (match): Match each stream operation with its time complexity, assuming a standard implementation on a sequential stream of n elements.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-streams-api** (assemble): Assemble the method signature for the Stream API terminal operation that collects elements into a mutable result container using a Collector. Use the tokens provided.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-string-pool** (assemble): Assemble the definition of the String pool by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-string-pool** (match): Match each operation to its time complexity in the HotSpot JVM, assuming a standard implementation with no extra memory constraints.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-string-vs-stringbuilder-vs-stringbuffer** (assemble): Assemble the line that correctly builds a string in a single-threaded method by appending to a mutable buffer.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-string-vs-stringbuilder-vs-stringbuffer** (assemble): Assemble the method signature for the StringBuilder class's append method that appends a String and returns the builder itself.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-string-vs-stringbuilder-vs-stringbuffer** (pick_one): Consider the following Java code:

```java
String s = "a";
for (int i = 1; i < 5; i++) {
    s += i;
}
System.out.println(s);
```

What is the output?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-strings** (assemble): Assemble the Java statement that correctly compares two String objects by their character content, not by reference identity. Use the tokens below to form the line.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-strings** (assemble): Assemble the Java method signature for checking whether two strings are equal, ignoring case differences. Use the tokens below to form the correct signature.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-strings** (assemble): Assemble the definition of a Java String from the tokens below. Place the tokens in the correct order to form a complete, accurate definition.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-strings** (pick_one): Consider the following Java code:

```java
String s = "hello";
s.toUpperCase();
System.out.println(s);
```

What is the output?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'HELLO'

- **java-strings** (grid_toggle): Consider the following operations on Java strings. For each operation, select the cell if the stated time complexity is correct for a typical implementation, assuming the string has length n and the operation is performed once (not in a loop).
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-strings** (order): Order the following steps to correctly implement a method that checks whether two strings are rotations of each other, assuming both strings are non-null and have the same length. The steps are shuffled.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-thread-lifecycle** (match): Match each Java thread state to the API call or condition that causes a thread to enter it.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-thread-lifecycle** (match): Match each Java thread state with the API call or condition that causes a thread to enter it. Assume standard Java semantics and no interrupts or spurious wakeups.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **linked-list** (assemble): Assemble the line that reverses a singly linked list in place, using the standard three-pointer approach. The line should be the core pointer update inside the loop, written as a single statement. Assume the variables prev, curr, and next are already declared.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **math-geometry** (grid_toggle): For each of the following operations on an n×n matrix, select the cells that correctly describe its time complexity and extra space complexity. Assume standard in-place implementations where applicable.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **prefix-sum** (order): Arrange the steps to count the number of subarrays with sum exactly k using prefix sums and a hash map, in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **prefix-sum** (assemble): Assemble the line that computes the sum of the subarray from index l to r inclusive, using the prefix sum array P.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **prefix-sum** (match): Match each operation on a static array of n elements with its time complexity using prefix sums (or the related difference array). Assume standard implementations and no extra data structures beyond the prefix/difference arrays.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-acid-vs-base** (match): Match each system or scenario with the most appropriate consistency model or design choice. Assume standard implementations and that the business impact of stale or lost data is the deciding factor.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-acid-vs-base** (self_rate): Name the four properties guaranteed by ACID transactions.
  - Gate said: wrong_format: The honest answer is a list of four items, which does not fit the self_rate format.

- **sd-acid-vs-base** (grid_toggle): Select the cells that correctly describe each consistency model. Assume standard definitions of ACID and BASE.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-acid-vs-base** (match): Match each consistency model with its typical database example.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-acid-vs-base** (order): Arrange the following steps in the correct order for handling a view event in a Redis-based 'users currently viewing page' feature, as described in the lesson. The steps are: (A) ZADD the user's ID with the current timestamp to the page's sorted set; (B) ZCARD to get the count of unique users in the window; (C) ZREMRANGEBYSCORE to remove entries older than 5 minutes. Assume the user is already authenticated and the page ID is known.
  - Gate said: refers to unseen material: 'the lesson'

- **sd-acid-vs-base** (order): Arrange the following steps in the correct order for implementing a sliding 5-minute unique viewer count for a page using Redis, as described in the lesson. Start with the first step when a user views the page.
  - Gate said: refers to unseen material: 'the lesson'

- **sd-cache-eviction-policies** (match): Match each cache eviction policy to the item it removes when the cache is full.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-circuit-breaker** (match): Match each circuit breaker state to its behavior.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-consistency-models** (pick_one): A distributed key-value store uses N=3 replicas, W=2, R=2, and reads return the highest version among the R replicas contacted. A client writes value X with version 10 to replicas A and B, and both acknowledge. Immediately after, the client reads from replicas A and C. What value does the read return?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'X'

- **sd-consistency-models** (grid_toggle): Which combinations of consistency model and replication mechanism correctly describe how the system achieves that model? Select all cells that hold.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-distributed-key-value-store** (grid_toggle): A distributed key-value store uses consistent hashing with virtual nodes, replication factor N=3, and quorum sizes R and W. Which combinations of R and W guarantee that every read quorum overlaps with every write quorum? Select all cells that hold.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-design-a-file-storage-service** (pick_one): A file storage service uses a control plane with metadata in a relational database and a data plane in a cloud object store. Clients upload via presigned URLs, and large files use multipart upload. The service marks a file 'ready' only after the multipart completion succeeds. Popular downloads are cached in a CDN with a cache key that includes the file version. Under a sudden spike in uploads of large files, which component is most likely to become the bottleneck first, assuming the object store scales elastically and the CDN is not involved in uploads?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'The CDN'

- **sd-design-a-file-storage-service** (self_rate): Name the cloud object stores mentioned in the lesson that provide strong read-after-write consistency for object PUT and DELETE.
  - Gate said: refers to unseen material: 'the lesson'

- **sd-design-a-news-feed** (bucket): Classify each item by the layer of the news feed system where it primarily belongs: Write Path, Read Path, or Shared/Supporting. Items are shuffled.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-design-a-ride-sharing-service** (pick_one): Which protocol should the driver app use to send its location updates to the backend?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'gRPC'

- **sd-design-a-ride-sharing-service** (match): Match each ride-sharing subsystem with the guarantee it must provide.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-url-shortener** (pick_one): You are designing a URL shortener that must guarantee accurate click analytics for every redirect, even when the same short link is clicked repeatedly by the same browser. Which redirect strategy should you use?
  - Gate said: guessable by shape: an option is far shorter than the rest: '301 Moved Permanently'

- **sd-design-search-autocomplete** (pick_one): Which data structure is most appropriate for serving search autocomplete suggestions for a typed prefix?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'Trie'

- **sd-design-search-autocomplete** (bucket): Classify each design decision for a search autocomplete system as belonging to the serving path, the write path, or both. Assume a standard production design: a trie with precomputed top-K lists per prefix, materialized prefix records sharded by consistent hashing of the prefix, an LRU cache for hot prefixes, and batch index rebuilds with atomic swaps.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-search-autocomplete** (bucket): Classify each design decision for a search autocomplete system as belonging to the serving path or the batch update path. Assume a standard production design: a trie with precomputed top-K lists per prefix, materialized prefix records sharded by consistent hashing of the prefix, and an LRU cache for hot prefixes.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-event-sourcing** (match): Match each event sourcing concept to its description.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-event-sourcing** (order): Rank the following steps for serving a read of an aggregate's current state in event sourcing, from first to last, assuming snapshots are used and the aggregate has a long event history.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-event-sourcing** (match): Match each event sourcing failure mode to its root cause.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-high-availability** (match): Match each availability level to its approximate allowed downtime per year.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-jwt** (bucket): Classify each item as belonging to the JWT header, the JWT payload, or the JWT signature.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-sharding-strategies** (match): Match each sharding strategy to its primary characteristic.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-sql-vs-nosql** (order): Arrange the following steps in the correct order for deciding between SQL and NoSQL for a new service, based on the lesson's guidance.
  - Gate said: refers to unseen material: 'the lesson'

- **sd-sql-vs-nosql** (match): Match each database type to its typical use case.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-sql-vs-nosql** (match): Match each database type to the workload it is best suited for, assuming standard implementations and typical access patterns.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **simulation** (grid_toggle): For each of the following simulation problems, select the cells that correctly describe its time complexity, assuming the standard implementation described in the lesson. Rows are problems, columns are complexities.
  - Gate said: refers to unseen material: 'the lesson'

- **simulation** (assemble): Assemble the line that checks whether a number is divisible by 15 in a FizzBuzz simulation. The line must evaluate the most specific combined condition before the individual parts.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sliding-window** (assemble): Assemble the line that initializes the sliding window state for finding the maximum sum of any contiguous subarray of length k in an array nums. The window sum is maintained as a variable. Assume nums is a list of integers and k is a positive integer.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-aggregate-functions** (match): Match each SQL aggregate function or expression with its behavior regarding NULLs and empty sets. Assume standard SQL semantics.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-case-expression** (order): Order the steps to correctly use CASE for conditional aggregation in a SQL query, from first to last.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-case-expression** (order): Arrange the following steps in the correct order to write a SQL query that pivots rows to columns using CASE and MAX, as described in the lesson. Assume the source table is Scores(StudentName, Subject, Score) and the desired output has one row per student with columns for Math and Science.
  - Gate said: refers to unseen material: 'the lesson'

- **sql-constraints** (tap_in_place): Which line contains the bug?
  - Gate said: not answerable: The question references a bug but no code snippet is provided.

- **sql-ctes** (bucket): Classify each statement about CTEs as applying to SQL Server, Oracle, PostgreSQL, or MySQL. Assume standard behavior for each engine as described in the lesson, and consider only the features explicitly mentioned. Each statement belongs to exactly one engine.
  - Gate said: refers to unseen material: 'the lesson'

- **sql-ctes** (assemble): Assemble the recursive CTE clause that combines the anchor and recursive members in SQL Server or Oracle. The tokens are shuffled; arrange them in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-ctes** (assemble): Assemble the SQL clause that combines the anchor and recursive members of a recursive CTE in SQL Server and Oracle. Use all tokens exactly once.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-null-handling** (claim_grid): For each statement about SQL NULL handling, mark it as true or false.
  - Gate said: not answerable: No statements are listed to mark as true or false.

- **sql-null-handling** (order): Rank these SQL NULL-handling functions by how many arguments they accept, from fewest to most. Assume standard SQL semantics; for functions with a variable number of arguments, use the minimum required.
  - Gate said: not answerable: No functions are listed to rank.

- **sql-null-handling** (order): Order the following steps to correctly handle a NULL in a SQL WHERE clause when you want to filter rows where a column is NULL, and then replace NULLs with a default in the SELECT list. Assume standard SQL.
  - Gate said: not answerable: No steps are provided to order.

- **sql-null-handling** (bucket): Classify each SQL expression or statement by whether it correctly tests for NULL or incorrectly uses a comparison operator with NULL. Assume standard SQL semantics.
  - Gate said: not answerable: No items are listed to classify.

- **sql-null-handling** (tap_in_place): Which line contains the bug?
  - Gate said: not answerable: No code snippet is provided to identify the buggy line.

- **sql-null-handling** (assemble): Assemble the SQL WHERE clause that correctly filters rows where the column `manager_id` is NULL. Use the tokens provided.
  - Gate said: not answerable: No tokens are provided to assemble.

- **sql-null-handling** (assemble): Assemble the SQL predicate that correctly tests whether a column contains NULL. Use all tokens exactly once.
  - Gate said: not answerable: No tokens are provided to assemble.

- **sql-null-handling** (pick_one): In SQL, which predicate correctly tests whether a column contains NULL?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-query-performance-tuning** (pick_one): A SQL Server query is slow because it performs a clustered index scan on a large table. The WHERE clause is `WHERE YEAR(OrderDate) = 2024`, and there is a nonclustered index on OrderDate. Which approach is the most appropriate first step to enable an index seek?
  - Gate said: guessable by shape: one option is the only one carrying code: "Rewrite the predicate as `WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01'`."

- **sql-query-performance-tuning** (grid_toggle): Consider a SQL Server query that is slow. You have identified the following possible root causes and the following possible fixes. For each cell, decide whether the fix is appropriate for that root cause. Assume standard SQL Server behavior and that the fix is applied as the primary remedy. Select all cells where the fix is appropriate.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-query-performance-tuning** (assemble): A SQL Server query is slow because the predicate `WHERE YEAR(OrderDate) = 2024` prevents an index seek on OrderDate. Assemble the rewritten WHERE clause that enables an index seek.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-relational-database-fundamentals** (assemble): Assemble the SQL clause that defines a foreign key constraint referencing the `customers` table's `id` column, with ON DELETE CASCADE behavior. Use all tokens exactly once.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-relational-database-fundamentals** (tap_in_place): A developer writes this SQL to create a table for storing orders. Which line contains the error that violates relational database integrity constraints?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-relational-database-fundamentals** (assemble): Assemble the definition of third normal form (3NF) from the tokens below. Assume the standard definition from relational database theory.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-relational-database-fundamentals** (bucket): Sort each item into the bucket that best describes its role in a relational database schema. Buckets: 'Primary key', 'Foreign key', 'Neither'.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-running-totals-and-moving-averages** (order): Arrange the following steps in the correct order to compute a running total using a window function in SQL. Assume the table DailySales has columns SaleDate and Amount, and the result should include every original row with a cumulative sum ordered by SaleDate.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-running-totals-and-moving-averages** (assemble): Assemble the SQL window frame clause for a running total that includes all rows from the start of the partition through the current row, using physical row ordering. Assume the ORDER BY column is unique, so no tie-breaker is needed.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-running-totals-and-moving-averages** (pick_one): You need a 7-day moving average of daily sales. The table has one row per date, but some dates are missing. Which frame clause should you use to ensure the window covers exactly the last 7 calendar days, assuming the database supports date intervals?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-running-totals-and-moving-averages** (assemble): Assemble the SQL window function clause that computes a running total of Amount ordered by SaleDate, using a ROWS frame from the start of the partition to the current row. The clause should be exactly:
SUM(Amount) OVER (ORDER BY SaleDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
Arrange the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-triggers** (bucket): Classify each trigger-related statement by the DBMS it describes. Assume standard behavior as described in the lesson; for PostgreSQL, consider row-level triggers and non-deferred constraints unless stated otherwise.
  - Gate said: refers to unseen material: 'the lesson'

- **sql-triggers** (bucket): Classify each trigger-related statement by the database system it describes. Assume standard behavior as described in the lesson: SQL Server DML triggers are statement-level with inserted/deleted pseudo-tables; PostgreSQL supports row-level and statement-level triggers with OLD/NEW; MySQL supports only row-level BEFORE and AFTER triggers on tables.
  - Gate said: refers to unseen material: 'the lesson'

- **sql-triggers** (assemble): Assemble the SQL Server trigger header that fires once per statement after an UPDATE on the Employees table, auditing salary changes. Use the tokens below in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **stack** (assemble): Assemble the line that pushes an element onto a stack implemented with an array, where `top` is the index of the next free slot and `size` is the current number of elements. The stack has capacity `capacity`.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **stack** (assemble): Assemble the line that pushes an element onto a stack implemented with a fixed-size array, assuming the stack is not full. Use the token pool below.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **stack** (pick_one): Which operation is NOT supported by a standard stack?
  - Gate said: guessable by shape: an option is far longer than the rest: 'Random access to middle elements'

- **stack** (order): Arrange the following steps in the correct order to evaluate a Reverse Polish Notation expression using a stack. Assume the expression is valid and operators are binary.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **stack** (match): Match each stack operation or pattern to its time complexity or key property, assuming standard array-backed stack implementations and the described algorithm.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **stack** (pick_one): Consider the following sequence of stack operations on an initially empty stack: push(5), push(3), pop(), push(7), push(2), pop(), pop(), push(9). What is the final state of the stack, listed from bottom to top?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **stack** (match): Match each stack operation with its time complexity in a standard array-backed stack implementation.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **stack** (pick_one): Which of the following operations is NOT supported by a standard stack?
  - Gate said: guessable by shape: an option is far longer than the rest: 'accessing an element in the middle'

- **trees** (assemble): Assemble the line that defines the recursive function to compute the maximum depth of a binary tree. The function takes a TreeNode root and returns an int. Use the tokens below to form the correct line.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **trees** (match): Match each tree operation with its time complexity in the worst case for a plain binary search tree (not necessarily balanced).
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **tries** (grid_toggle): Consider a standard trie storing n words over a lowercase English alphabet, where L is the length of the word or prefix being processed. Select the cells that correctly describe the time complexity of each operation.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **tries** (match): Match each trie operation with its time complexity, assuming a standard trie implementation where each node stores child links in a structure with O(1) lookup (e.g., fixed-size array or hash map).
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **tries** (pick_one): Which operation on a trie requires the final node to be marked as terminal?
  - Gate said: guessable by shape: an option is 'All of the above'

- **tries** (order): Arrange the following steps in the correct order for inserting the word 'apple' into a trie that already contains the word 'app' (with 'app' marked as terminal).
  - Gate said: guessable by elimination: 2/3 samples flagged it

## Cards the gate caught and the rewrite fixed

These are the questions as first written. The gate objected, a rewrite pass replaced each one, and the replacement passed - so these are not in the app. They are here because the gate is on trial too: if its objections below look wrong, it is throwing away good work, and if they look right, it is earning its cost.

- **1-d-dynamic-programming** (assemble): Assemble the recurrence line for the Climbing Stairs problem, where dp[i] is the number of distinct ways to reach step i. Use the tokens below to form the line that computes dp[i] from earlier values.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **1-d-dynamic-programming** (pick_one): In the House Robber problem, you have an array nums of non-negative integers representing the amount of money in each house. You cannot rob two adjacent houses. Consider the standard 1-D DP solution with dp[i] = max(dp[i-1], dp[i-2] + nums[i-1]), where dp[i] is the maximum amount for the first i houses. Suppose you change the recurrence to dp[i] = max(dp[i-1], dp[i-2] + nums[i]) (using nums[i] instead of nums[i-1]). What is the consequence of this change?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **1-d-dynamic-programming** (assemble): Assemble the line that updates the maximum product subarray DP state for the current element `num` in the standard O(n) solution. The line should compute the new `max_prod` and `min_prod` using the previous values and the current number. Assume `num` is an integer and the previous `max_prod` and `min_prod` are available.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **1-d-dynamic-programming** (pick_one): Which of the following is a counterexample showing that a greedy approach of always robbing the current house if it is not adjacent to the last robbed house fails for the House Robber problem?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **1-d-dynamic-programming** (match): Match each 1-D DP problem with the recurrence or state definition that solves it.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **2-d-dynamic-programming** (match): Match each 2-D DP problem with the operation that dominates its time complexity, assuming standard implementations and input sizes m, n (strings/grid dimensions) or n (array length).
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **2-d-dynamic-programming** (assemble): Assemble the line that defines the recurrence for the Longest Common Subsequence DP table, where dp[i][j] is the LCS length for prefixes text1[0:i] and text2[0:j]. The line should be valid Python code.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **2-d-dynamic-programming** (order): Arrange the following steps in the correct order for filling a 2-D DP table for the Longest Common Subsequence problem, assuming the table is indexed from 0 to m and 0 to n, and the strings are text1 and text2.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **2-d-dynamic-programming** (match): Match each 2-D dynamic programming problem with the operation that dominates its time complexity, assuming standard implementations and no extra constraints.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **advanced-graphs** (assemble): Assemble the line that initializes the distance array for Dijkstra's algorithm in a graph with V vertices, where all edge weights are non-negative and the source vertex is 0. Use the tokens below.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **advanced-graphs** (match): Match each algorithm to its time complexity, assuming a standard implementation with a binary heap where applicable.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **arrays-hashing** (order): Arrange the following steps to solve Two Sum in O(n) time using a hash map, in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **arrays-hashing** (match): Match each operation to its time complexity for the given data structure.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **arrays-hashing** (assemble): Assemble the line that computes the address of element i in a contiguous array, given base address, index i, and element size.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **arrays-hashing** (match): Match each operation with its correct time complexity for the given data structure and scenario.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **bit-manipulation** (match): Match each bit-manipulation operation to its time complexity for a single call on a 32-bit integer, assuming a standard implementation and no precomputation.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-critical-section-problem** (order): Arrange the following steps in the order a process follows when using a critical section solution, from first to last.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-critical-section-problem** (assemble): Assemble the definition of the progress condition for the critical section problem using the tokens below. Arrange the tokens in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-critical-section-problem** (order): Arrange the following steps in the order a process follows when using a critical section solution, from requesting entry to completing exit.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-file-systems** (match): Match each filesystem concept to the error or misconception a candidate might state about it.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-http-https** (match): Match each HTTP status code to its meaning.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-http-https** (assemble): Assemble the definition of HTTP as a stateless request/response protocol. Arrange the tokens to form a correct one-sentence definition.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-locking-mechanisms** (match): Match each locking mechanism or concept to the problem it is most directly associated with.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-locking-mechanisms** (assemble): Assemble the SQL clause used in pessimistic locking to acquire a row-level lock before reading or modifying a row, ensuring other transactions cannot modify it until the lock is released.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-normalization** (assemble): Assemble the definition of 3NF by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-object-oriented-programming-principles** (order): Arrange the following steps in the order they occur when a Java program calls an overridden method on a subclass instance via a superclass reference. Assume standard JVM dynamic dispatch.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-object-oriented-programming-principles** (assemble): Assemble the definition of encapsulation in object-oriented programming from the tokens below.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-osi-model** (assemble): Assemble the definition of the OSI model by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-osi-model** (order): Arrange the following steps in the order they occur when a host sends an HTTP request over TCP/IP, from the application layer down to the physical medium.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-osi-model** (match): Match each OSI layer to the error or issue that would be diagnosed at that layer.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-paging-and-virtual-memory** (match): Match each paging-related error or scenario with its most likely cause.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-processes-vs-threads** (pick_one): Which statement about processes and threads is NOT true?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-processes-vs-threads** (assemble): Assemble the definition of a thread by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-subnetting-and-cidr** (assemble): Assemble the definition of a subnet mask in IPv4 networking.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-synchronization-primitives** (assemble): Assemble the definition of a mutex from the tokens below.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-tcp-flow-and-congestion-control** (match): Match each TCP mechanism or parameter with its correct description. Assume standard Reno-style TCP and RFC 6928 initial window.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-tcp-vs-udp** (pick_one): A developer builds a live video streaming application that sends frames over UDP. During a network congestion event, the sender keeps transmitting at a constant high bitrate, and the receiver experiences increasing packet loss. The developer observes that the video quality degrades severely and the network becomes even more congested. What is the most likely cause of this degradation?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-tcp-vs-udp** (match): Match each protocol behavior to the protocol that exhibits it.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-tcp-vs-udp** (match): Match each transport protocol characteristic to the protocol it describes.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **cs-tlb-and-caching** (order): Order the following events in the typical sequence when a CPU performs a load that misses in the L1 cache and the TLB, assuming a hardware page-walker and a physically indexed L2 cache. Start from the load instruction issuing.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **cs-transaction-isolation-levels** (match): Match each isolation level to the anomaly it permits under the ANSI SQL standard, assuming a standard implementation without MVCC snapshot extensions.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **design** (match): Match each design problem to the operation complexity of its standard implementation, assuming monotonic timestamps where relevant and standard data structures.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **design** (assemble): Assemble the line that defines the HitCounter class using a deque of (timestamp, count) pairs, assuming timestamps are monotonically increasing. The line should declare the deque as a private member.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **design** (match): Match each design problem to the backing structure that gives the required time complexity under the stated assumptions. Assume timestamps are monotonic for Hit Counter and Logger Rate Limiter, and that getHits is called with non-decreasing timestamps.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **greedy** (order): Order the following steps of a typical greedy algorithm from first to last.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **greedy** (assemble): Assemble the line that implements the greedy choice in Kadane's algorithm for Maximum Subarray: update the current suffix sum by either extending the previous suffix or starting fresh at the current element.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **greedy** (match): Match each greedy algorithm with its time complexity, assuming standard implementations and input size n.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **intervals** (assemble): In Merge Intervals, after sorting intervals by start time, we merge overlapping intervals. Complete the line that checks whether the current interval overlaps with the last merged interval. Assume intervals are represented as lists [start, end], and touching endpoints count as overlapping.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **intervals** (match): Match each interval problem to its time complexity, assuming the standard optimal algorithm and that n is the number of intervals and q is the number of queries.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **intervals** (match): Match each interval algorithm to its time complexity, assuming n intervals and q queries, with standard implementations.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-arraylist-vs-linkedlist** (match): Match each performance issue with its most likely cause when using ArrayList or LinkedList in Java.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-concurrenthashmap** (match): Match each ConcurrentHashMap behavior or design choice with the reason it is implemented that way. Assume Java 8+ semantics.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-concurrenthashmap** (match): Match each ConcurrentHashMap behavior or design choice with the reason it exists.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-default-and-static-interface-methods** (assemble): Assemble the line that declares a default method named greet in an interface, returning a String "Hello". Use the tokens below.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-default-and-static-interface-methods** (match): Match each Java interface method scenario with the error or outcome it causes.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-exceptions** (assemble): Assemble the method signature for a method that reads a file and declares the checked exception it may throw. The method is named readFile, takes a String parameter named path, and returns a String. Use the tokens below to form the complete signature.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-fail-fast-vs-fail-safe-iterators** (match): Match each Java iterator type or collection to the behavior it exhibits when its backing collection is structurally modified during iteration. Assume standard implementations and single-threaded modification unless noted.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-fail-fast-vs-fail-safe-iterators** (assemble): Assemble the line that creates an iterator over an ArrayList and then calls next() on it, using the tokens below. The line should be valid Java and should not throw an exception when the list is unmodified.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-garbage-collection** (pick_one): In HotSpot's generational heap, where are new objects allocated?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'Eden'

- **java-garbage-collection** (match): Match each HotSpot garbage collector to its primary operational characteristic, assuming standard implementations and typical workloads.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-garbage-collection** (assemble): Assemble the Java statement that requests garbage collection, using the tokens below. The statement should be a single line that calls the method on the Runtime instance.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-garbage-collection** (tap_in_place): Which line contains the unsafe assumption about garbage collection?

1. System.gc();
2. // assume all garbage is collected immediately
3. byte[] data = new byte[1024];
4. data = null;
5. // data is now unreachable and will be freed at the next GC
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-generics** (assemble): Assemble the method signature for a generic method that copies elements from a source list into a destination list, following the PECS rule. The method is static and named copy. Use the tokens provided.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-generics** (assemble): Assemble the Java method signature for a generic utility that copies elements from one list to another, following the PECS rule. The method is static and returns void. Use the tokens provided.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-hashmap-internals** (match): Match each HashMap operation with its worst-case time complexity in Java 8+, assuming a standard implementation with default load factor and no pathological hashCode that maps all keys to the same bucket.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-heap-vs-stack** (match): Match each JVM memory error or situation to its most likely cause.
  - Gate said: not answerable: The items to match are not provided.

- **java-heap-vs-stack** (claim_grid): Mark each statement as true or false.
  - Gate said: not answerable: The question references a claim grid but no statements are provided.

- **java-heap-vs-stack** (match): Match each JVM memory-related operation or scenario with its typical complexity or failure mode. Assume standard HotSpot JVM behavior with default settings and no escape analysis optimizations.
  - Gate said: not answerable: The items to match are not provided.

- **java-heap-vs-stack** (assemble): Assemble the line of Java code that declares a local variable `p` of type `Point` and initializes it with a new `Point` object whose `x` is 3 and `y` is 4. Use the tokens below. The object is allocated on the heap, while the reference `p` lives in the current stack frame.
  - Gate said: not answerable: The tokens to assemble are not provided.

- **java-heap-vs-stack** (assemble): Assemble the definition of the Java heap by arranging the tokens in the correct order.
  - Gate said: not answerable: The tokens to assemble are not provided.

- **java-heap-vs-stack** (order): Order the following events in the lifetime of a Java object from creation to reclamation, assuming the object is created inside a method, a reference to it is stored in a local variable, and the method returns without storing the reference anywhere else.
  - Gate said: not answerable: The events to order are not provided.

- **java-heap-vs-stack** (match): Match each JVM memory scenario with the error or outcome it produces. Assume standard HotSpot behavior with default settings and no escape analysis optimizations.
  - Gate said: not answerable: The items to match are not provided.

- **java-heap-vs-stack** (grid_toggle): Consider a Java program with a method that creates a local object and a local primitive. Which cells correctly describe where each item is stored and how its memory is reclaimed? Select all cells that are true.
  - Gate said: not answerable: The grid cells are not provided.

- **java-heap-vs-stack** (assemble): Assemble the Java method signature that declares a method named `process` taking an `int` parameter and returning nothing. Use all tokens.
  - Gate said: not answerable: The tokens to assemble are not provided.

- **java-immutability** (assemble): Assemble the line that makes this class immutable by preventing mutation of the internal Date field. The line is the getter method body. Tokens are shuffled; arrange them in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-immutability** (assemble): Assemble the definition of an immutable object in Java by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-inheritance-vs-composition** (assemble): Assemble the Java method signature for a class that implements the Runnable interface and declares a public run method with no parameters and no return value.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-inheritance-vs-composition** (order): Arrange the following steps in the correct order to refactor a class hierarchy to favor composition over inheritance, as recommended by the design principle. Assume the goal is to reduce coupling and allow runtime behavior changes.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-inheritance-vs-composition** (assemble): Assemble the line that declares a class `Car` that has-a `Engine` using composition, with the engine as a private final field.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-inheritance-vs-composition** (assemble): Assemble the definition of composition in Java by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-java-8-features** (assemble): Assemble the method signature for the functional interface Predicate from java.util.function, as it would be declared in Java 8. Use the tokens provided.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-java-8-features** (assemble): Assemble the Java 8 code that creates a stream from a list of strings, filters out empty strings, and collects the remaining strings into a new list. Use the tokens provided.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-java-8-features** (assemble): Assemble the definition of a functional interface in Java 8 by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-jdbc** (numeric): Consider a JDBC application that executes a batch of N INSERT statements using a single PreparedStatement. The application calls addBatch() N times, then calls executeBatch() once. Assume the driver returns an update count of 1 for each successfully inserted row, and no exceptions occur. What is the total number of rows inserted into the database?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-jdbc** (grid_toggle): Classify each JDBC API method by its primary return type. Select all cells that are correct.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-jdbc** (assemble): Assemble the JDBC method signature for executing a parameterized SQL statement that returns a ResultSet, using the tokens below. The method belongs to PreparedStatement and takes no arguments.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-jdbc** (assemble): Assemble the line that executes a parameterized SQL INSERT using a PreparedStatement and returns the number of rows affected. Use all tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-jvm-and-memory** (assemble): Assemble the JVM option that caps the native memory used for class metadata since Java 8. Use all tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-jvm-and-memory** (match): Match each JVM memory issue with its most likely cause.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-jvm-and-memory** (assemble): Assemble the JVM flag that caps the size of Metaspace in Java 8 and later.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-lock-interface-and-reentrantlock** (assemble): Assemble the correct line for acquiring a ReentrantLock and releasing it in a finally block, using the tokens below. The lock variable is named `lock`.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-lock-interface-and-reentrantlock** (assemble): Assemble the correct usage pattern for a ReentrantLock that guarantees the lock is released even if the critical section throws an exception. Use all tokens in the correct order.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-lock-interface-and-reentrantlock** (assemble): Assemble the correct usage pattern for acquiring and releasing a ReentrantLock in Java, ensuring the lock is released even if an exception occurs. Use all tokens exactly once.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-lock-interface-and-reentrantlock** (match): Match each Lock/ReentrantLock operation or concept with its time complexity or behavioral characteristic, assuming a standard OpenJDK implementation and no contention.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-oop-concepts** (pick_one): Consider the following Java code:

```java
class Shape {
    double area() { return 0; }
}

class Circle extends Shape {
    double area() { return 3.14 * 2 * 2; }
}

class Square extends Shape {
    double area() { return 3 * 3; }
}

public class Main {
    public static void main(String[] args) {
        Shape s = new Circle();
        System.out.println(s.area());
    }
}
```

What is the output?
  - Gate said: guessable by shape: an option is far shorter than the rest: '0'

- **java-oop-concepts** (assemble): Assemble the definition of encapsulation in Java by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-optional** (assemble): Assemble the line that creates an Optional from a possibly-null value.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-optional** (assemble): Assemble the method signature for creating an Optional that accepts a possibly null value and returns an empty Optional when the value is null.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-optional** (assemble): Assemble the definition of Optional from the Java standard library by arranging the tokens in the correct order. The definition should read: a container object which may or may not contain a non-null value.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-optional** (pick_one): Given the following Java code, what is printed?

Optional<String> opt = Optional.of("hello");
String result = opt.map(s -> null).orElse("fallback");
System.out.println(result);
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-polymorphism** (assemble): Assemble the line that declares a method in a subclass which overrides a superclass method with the same name and parameter list, using a covariant return type. The superclass method is:

```java
public Animal getPet() { ... }
```

and the subclass method should return a Dog (a subtype of Animal).
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-polymorphism** (assemble): Assemble the method signature that correctly overrides the inherited method `public void speak()` in a subclass, using the tokens below. The signature must be a valid Java override.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-polymorphism** (match): Match each Java polymorphism scenario with the correct resolution behavior. Assume standard Java semantics and that all code compiles.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-polymorphism** (order): Arrange the following steps in the order Java uses to resolve a method call on a superclass reference pointing to a subclass object, from first to last.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-polymorphism** (assemble): Assemble the definition of method overriding in Java using the tokens below. The definition must state what overriding is and how the JVM dispatches the call.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-polymorphism** (pick_one): Consider the following Java code:

class Animal {
    void speak() { System.out.println("Animal speaks"); }
}

class Dog extends Animal {
    void speak() { System.out.println("Woof"); }
    void speak(int times) { for (int i = 0; i < times; i++) System.out.println("Woof"); }
}

public class Test {
    public static void main(String[] args) {
        Animal a = new Dog();
        a.speak();
    }
}

What is the output?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'Woof'

- **java-serialization** (assemble): Assemble the line that declares the serialVersionUID for a Serializable class.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-serialization** (pick_one): Which interface must a Java class implement to be serialized using the built-in Java serialization mechanism?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-serialization** (assemble): Assemble the definition of Java serialization by arranging the tokens in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-thread-lifecycle** (assemble): Assemble the definition of the BLOCKED state in the Java thread lifecycle using the tokens below. The definition should read as a single sentence.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-thread-lifecycle** (assemble): Assemble the method signature for starting a Java thread, using the tokens below. The signature is the instance method on Thread that creates the native thread and transitions the thread from NEW to RUNNABLE.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-thread-lifecycle** (assemble): Assemble the line that transitions a newly created Thread object from NEW to RUNNABLE, using the tokens below. The line should call the method that creates the underlying OS thread.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-volatile-keyword** (assemble): Assemble the Java declaration that marks a field as volatile, using the tokens below. The declaration is for a field named `running` of type `boolean`.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **java-volatile-keyword** (assemble): Assemble the Java field declaration that makes the `running` flag visible across threads without using locks. The line should declare a boolean field named `running` with an initial value of `true`.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **java-wait-notify-notifyall** (assemble): Assemble the line of code that correctly waits on the object's monitor while holding its intrinsic lock, using the standard condition-loop pattern. The line should be a single statement that calls wait() only when the condition is false. Tokens:
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **linked-list** (match): Match each linked list operation with its time complexity, assuming a singly linked list with only a head pointer and no tail pointer, and that we have a pointer to the node to be deleted (not its predecessor).
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **linked-list** (match): Match each linked-list problem to the pattern trick that best solves it in the stated constraints. Assume standard singly linked lists and the constraints given in the problem statements.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **linked-list** (order): Arrange the steps to reverse a singly linked list in place, in the order they are performed. Assume the list has at least one node and you have a pointer to the head.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **matrix-grid** (assemble): Assemble the line that checks whether a neighbor cell (nr, nc) is within the bounds of a grid with m rows and n columns. Use the tokens provided.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **matrix-grid** (match): Match each matrix operation with its time complexity, assuming a standard implementation on an m x n grid with no extra constraints.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-api-gateway** (tap_in_place): You are reviewing an API gateway configuration for a microservices deployment. The gateway handles authentication, rate limiting, and routing. Which line is the bottleneck that could cause a single point of failure?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-api-gateway** (match): Match each API gateway responsibility to its description.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-bloom-filters** (match): Match each Bloom filter operation or property with its guarantee.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-bloom-filters** (order): Rank the following steps in the order they occur when a Bloom filter is used as a pre-check before an exact lookup in a storage engine, from first to last. Assume the filter is already built and sized for the expected set.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-cache-strategies** (match): Match each cache write strategy to its guarantee about when a write is acknowledged.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-caching** (tap_in_place): A URL shortener service uses Redis as a cache in front of PostgreSQL. The following code handles a read request for a short code. Which line is the bottleneck that will cause the database to be hit on every request?

1. def get_long_url(short_code):
2.     long_url = redis.get(short_code)
3.     if long_url is None:
4.         long_url = db.query("SELECT long_url FROM urls WHERE short_code = ?", short_code)
5.         return long_url
6.     return long_url
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-caching** (order): Arrange the steps in the correct order for a cache-aside read path in a URL shortener service.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-caching** (match): Match each caching concept to its description.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-caching** (order): Order the steps for handling a cache read in a cache-aside pattern, from the initial request to the final response.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-cap-theorem** (grid_toggle): A distributed key-value store is deployed across two data centers. During a network partition, the system must choose between consistency and availability. For each combination of system behavior and CAP property, indicate whether the behavior satisfies that property during the partition. Assume the partition is ongoing and messages between data centers are dropped.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-cdn** (pick_one): Which type of content benefits most from being served through a CDN?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-consistent-hashing** (pick_one): You are designing a distributed cache with 10 physical nodes. You must choose between simple modulo hashing and consistent hashing with virtual nodes. The cache will be scaled up to 11 nodes under load, and the workload is uniform with no hot keys. Which approach minimizes the fraction of keys that must be remapped when the node is added?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-cqrs** (bucket): Classify each statement as belonging to the Command side or the Query side of a CQRS system. Assume a standard CQRS implementation where commands mutate state and queries return data.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-database-federation** (match): Match each database architecture term to its correct description.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-database-sharding** (match): Match each sharding mistake to the consequence it causes.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-database-sharding** (bucket): Classify each item as belonging to either 'Sharding' or 'Replication'.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-database-sharding** (match): Match each database concept with its correct description.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-chat-system** (bucket): Sort each item into the bucket that best describes its role in a chat system design. Assume a standard implementation with WebSocket gateways, a central presence registry, durable message storage, and push notifications for offline users.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-chat-system** (bucket): Classify each item into the correct bucket: 'Connection layer' or 'Message processing'.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-chat-system** (match): Match each delivery state to its definition.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-design-a-chat-system** (order): Arrange the steps in the correct order for delivering a message from Alice to Bob in a chat system, assuming Bob is online. Start with Alice sending the message.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-chat-system** (grid_toggle): In a chat system, which combinations of delivery mechanism and message state are correct? Assume standard implementations: WebSockets for online delivery, push notifications for offline delivery, and client acknowledgements for delivery/read receipts.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-notification-system** (grid_toggle): Which combinations of delivery method and delivery semantics are correct for a notification system? Assume standard implementations: mobile push uses FCM/APNs, in-app uses a WebSocket connection, and email/SMS use provider APIs.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-pastebin** (bucket): Classify each design decision by where it belongs in a pastebin architecture: Metadata Store, Object Storage, or Application Layer. Assume a standard implementation where the database holds only small indexed metadata and object storage holds the full paste content.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-pastebin** (bucket): Classify each design decision by whether it belongs to the metadata path or the content path in a pastebin system. Assume the standard architecture: a relational database stores metadata, and object storage stores paste content.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-design-a-pastebin** (grid_toggle): A pastebin service stores paste text in object storage and metadata in a database. Which combinations of operation and storage layer are correct for the standard design? Select all cells that hold.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-pastebin** (match): Match each API operation or component with the guarantee it provides in a pastebin design.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-rate-limiter** (order): Order the steps to implement a fixed window rate limiter using Redis, from receiving a request to returning a response. Assume the limit is 100 requests per minute per API key.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-design-a-rate-limiter** (bucket): Classify each component by the layer of the rate limiter it belongs to: client-side, server-side, or middleware.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-web-crawler** (match): Match each crawler component to its primary responsibility.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-design-a-web-crawler** (order): Order the steps a web crawler takes when processing a newly discovered URL, from first to last. Assume the URL is not already in the visited store and the domain is currently allowed by politeness.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-design-a-web-crawler** (bucket): Classify each URL canonicalization step as either 'Always safe' or 'Only if site semantics allow'. Assume the crawler must not merge URLs that could represent different resources.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-design-a-web-crawler** (tap_in_place): A crawler design uses a Bloom filter to reduce lookups to the visited store. Which line is the bottleneck that causes new URLs to be incorrectly skipped?
  - Gate said: not answerable: The question references a specific code snippet that is not provided.

- **sd-design-a-web-crawler** (bucket): Classify each component by the layer of the web crawler architecture it belongs to: URL frontier, fetcher, parser, or visited store. Assume a standard distributed crawler design.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-design-case-studies** (bucket): Classify each design decision as belonging to the write path or the read path of a payment system. Assume a standard integration on top of a payment provider like Stripe.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-distributed-cache** (match): Match each distributed cache technology or concept with its correct characteristic.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-distributed-transactions** (match): Match each distributed transaction concept with its description.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-grpc** (pick_one): You are designing a service that streams real-time market data updates to many connected clients. Each client subscribes to a set of symbols and receives a continuous stream of price ticks. The service must push updates to clients as soon as they occur, with minimal latency, and clients do not send any data after the initial subscription. Which gRPC RPC shape should you use?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'Unary'

- **sd-horizontal-scaling** (grid_toggle): A system is scaled horizontally by adding more machines behind a load balancer. Which of the following statements are true for a typical horizontally scaled system? Select all that apply.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-horizontal-scaling** (match): Match each horizontal scaling concept to its description.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-horizontal-scaling** (bucket): Classify each item as belonging to the application tier or the data tier in a horizontally scaled system. Assume a standard architecture where the application tier handles request logic and the data tier stores shared state.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-indexes** (match): Match each index type to the query pattern it best supports.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-layer-4-vs-layer-7-load-balancing** (pick_one): Which layer of load balancing can route HTTP requests based on the URL path, such as sending /api to one backend pool and /images to another?
  - Gate said: guessable by shape: an option is far shorter than the rest: 'Layer 4'

- **sd-load-balancing** (order): Arrange the steps in the order a load balancer performs them when a new request arrives and a backend server fails health checks. Assume the load balancer uses active health checks and least connections.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-load-balancing** (order): Arrange the steps in the correct order for a load balancer to handle a backend server failure and recover, assuming active health checks are used.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-load-balancing** (tap_in_place): A load balancer distributes traffic across three backend servers. Which line is the bottleneck in this setup?

1. All three servers are healthy and receive equal traffic via round robin.
2. Server A has 8 CPU cores, Server B has 4 CPU cores, Server C has 2 CPU cores.
3. The load balancer uses round robin without weights.
4. Health checks run every 10 seconds and mark a server unhealthy after 3 consecutive failures.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-microservices** (order): Order the steps for handling a search request in a microservices-based proximity search system (e.g., Yelp), assuming the search index is already built and up to date.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-microservices** (bucket): Classify each design decision as belonging to a microservices architecture or a monolithic architecture. Assume standard implementations: microservices use independent services with separate data stores and network communication; monoliths use a single deployable unit with a shared database.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-microservices** (bucket): Classify each communication or data pattern by the layer where it belongs in a microservices architecture: Service-to-Service Communication, Data Ownership, or Read Model.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-monitoring-and-observability** (match): Match each telemetry signal type with its primary purpose in a distributed system.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-n-1-query-problem** (match): Match each relationship cardinality to the most appropriate strategy for avoiding N+1 queries, assuming a standard ORM and that all related data is needed.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-n-1-query-problem** (grid_toggle): Consider a typical ORM-based application that fetches a list of parent entities and then accesses a related entity for each parent. For each combination of relationship cardinality and loading strategy, indicate whether the strategy is generally appropriate for avoiding the N+1 query problem without excessive data duplication. Assume the endpoint needs all fetched parent rows and their related data, and that the related data is actually used.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-nosql-types** (match): Match each NoSQL data model to its primary access pattern.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-nosql-types** (grid_toggle): Which combinations of NoSQL data model and operation are efficient as described? Select all cells that hold.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-object-storage** (match): Match each object storage operation or concept with the API guarantee or characteristic it provides.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-object-storage** (order): Order the steps a client takes to upload a large file to S3-compatible object storage using multipart upload, from first to last.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-publish-subscribe** (order): Order the steps to deliver a message to a subscriber using Redis Pub/Sub, from publish to subscriber processing.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-replication** (grid_toggle): Which combinations correctly describe how a single-leader replicated system handles a write under synchronous vs asynchronous replication? Select all cells that are true.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-rest-api** (order): Arrange the following steps in the correct order for a REST API server to handle a POST request that creates a new resource, assuming the request is valid and no conflict occurs.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-rest-api** (match): Match each HTTP method to its idempotency property in a standard REST API.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-sagas** (order): Order the steps of a saga's compensation flow after a failure occurs in a later step. Assume the saga has already committed earlier local transactions and the failure is detected by the orchestrator.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-service-discovery** (bucket): Classify each item as belonging to client-side discovery or server-side discovery.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-service-discovery** (match): Match each service discovery concept to its description.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-sharding-strategies** (tap_in_place): A system uses range sharding on a monotonically increasing timestamp key. Which line is unsafe?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-sharding-strategies** (grid_toggle): Consider a system that stores user records sharded by user ID. Which cells correctly describe the behavior of each sharding strategy? Select all cells that are true.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sd-sharding-strategies** (bucket): Classify each sharding strategy by its primary characteristic: efficient range scans, uniform point-lookup distribution, or flexible remapping via an external lookup service.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sd-unique-id-generation** (order): Arrange the following steps in the order a Snowflake worker generates IDs within a single millisecond, from first to last. Assume the worker has a valid unique worker ID and the clock is monotonic.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **segment-tree-fenwick** (match): Match each operation to its time complexity for a standard implementation on an array of size n, where the segment tree uses lazy propagation for range updates and the Fenwick tree supports point updates and prefix sums.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sliding-window** (match): Match each sliding-window problem to the state or invariant that makes its window update O(1).
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-aggregate-functions** (bucket): Classify each SQL aggregate function by its NULL handling behavior. Buckets: 'Ignores NULL inputs' and 'Counts rows including NULLs'.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-char-vs-varchar** (assemble): Assemble the SQL Server expression that returns the number of characters in the Code column, excluding trailing spaces. Use the tokens provided.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-clustered-vs-non-clustered-indexes** (assemble): Assemble the SQL statement that creates a non-clustered index on the CustomerID column of the Orders table, including the OrderDate and Amount columns to make it covering. Use the tokens provided.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-correlated-vs-nested-subqueries** (match): Match each SQL subquery pattern to its correct classification as correlated or non-correlated. Assume standard SQL semantics and that aliases are defined as shown.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-correlated-vs-nested-subqueries** (assemble): Assemble the SQL line that finds employees whose salary equals the maximum salary in their own department, using a correlated subquery. The line is:

SELECT name FROM employees e WHERE salary = (SELECT MAX(salary) FROM employees e2 WHERE e2.dept_id = e.dept_id)

Arrange the tokens in the correct order.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-correlated-vs-nested-subqueries** (assemble): Assemble the definition of a correlated subquery by arranging the tokens in the correct order. The definition must state that a correlated subquery references at least one column from an outer query and is logically evaluated once for each row of the outer statement.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-correlated-vs-nested-subqueries** (grid_toggle): Consider the following SQL statements. For each statement, determine whether the subquery is correlated or non-correlated. Assume standard SQL semantics and that all referenced tables and columns exist.

Statements:
1. SELECT name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);
2. SELECT name FROM employees e WHERE salary = (SELECT MAX(salary) FROM employees e2 WHERE e2.dept_id = e.dept_id);
3. SELECT name FROM employees WHERE dept_id IN (SELECT dept_id FROM departments WHERE location = 'NY');
4. SELECT name FROM employees e WHERE EXISTS (SELECT 1 FROM departments d WHERE d.dept_id = e.dept_id AND d.location = 'NY');
5. SELECT name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = employees.dept_id);
6. SELECT name FROM employees WHERE dept_id = (SELECT dept_id FROM departments WHERE location = 'NY' LIMIT 1);

Select all statements that contain a correlated subquery.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-covering-indexes** (tap_in_place): A developer wants to eliminate the Key Lookup in the execution plan for this query:

SELECT order_date, amount
FROM Orders
WHERE customer_id = 42;

They create the following index:

CREATE INDEX ix_orders_customer
ON Orders (customer_id, order_date, amount);

Which line of the index definition is the bug that prevents this index from being a covering index for the query?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-covering-indexes** (assemble): A SQL Server table Orders(id, customer_id, order_date, amount) has a nonclustered index on customer_id only. A query selects order_date and amount for a given customer_id, causing a Key Lookup for every matching row. Assemble the CREATE INDEX statement that makes the index covering for this query, using the token pool below.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-data-types** (grid_toggle): You are designing a SQL Server table for a multilingual product catalog. The catalog has three columns: product_code (always ASCII, exactly 10 characters), description (may contain emoji and other Unicode, up to 500 characters), and price (currency values with exactly 2 decimal places). For each column, select the most appropriate data type from the options. Assume a standard non-UTF8 collation and that all values fit within the specified limits.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-data-types** (match): Match each SQL Server data type term with its correct meaning. Assume standard SQL Server behavior with a non-UTF8 collation unless otherwise noted.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-ddl-dml-dcl-tcl** (match): Match each SQL statement category to its defining effect. Assume standard SQL terminology and a typical transactional engine such as PostgreSQL, where DDL can be rolled back.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-ddl-dml-dcl-tcl** (assemble): Assemble the definition of DDL (Data Definition Language) from the tokens below. The definition should state what DDL changes and list its main statements. Use all tokens exactly once.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-ddl-dml-dcl-tcl** (assemble): Assemble the SQL statement that removes all rows from the table `inventory` and resets any identity column, using the correct category of statement. The token pool is shuffled; arrange the tokens into a valid single statement.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-execution-plans** (numeric): In PostgreSQL, an EXPLAIN ANALYZE output shows a Nested Loop node with actual rows=5 and loops=200. What is the total number of rows emitted by this node across all loops?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-execution-plans** (bucket): Classify each statement as applying to EXPLAIN, EXPLAIN ANALYZE, or both in PostgreSQL.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-execution-plans** (match): Match each execution plan term with its correct meaning. Assume PostgreSQL EXPLAIN ANALYZE output unless stated otherwise.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-functions** (assemble): Assemble the SQL statement that creates an inline table-valued function named dbo.OrdersForCustomer that accepts an integer parameter @CustomerID and returns orders for that customer. The function body is a single SELECT returning OrderID, OrderDate, and Total from Sales.Orders where CustomerID equals the parameter. Use the tokens below.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-group-by-and-having** (bucket): Classify each SQL clause or expression by whether it operates before grouping (WHERE) or after grouping (HAVING). Assume standard SQL evaluation order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-index-seek-vs-scan** (assemble): Assemble the SQL Server predicate that makes this query SARGable, so the optimizer can use an Index Seek on the OrderDate index instead of an Index Scan. The query must return all orders from the year 2024.

SELECT * FROM Orders WHERE ___
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-inner-vs-outer-join** (bucket): Classify each SQL join type by its row-preservation behavior. Buckets: 'Preserves left rows only', 'Preserves right rows only', 'Preserves both sides', 'Preserves neither side'.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-inner-vs-outer-join** (assemble): Assemble the SQL clause that returns all rows from the left table and matching rows from the right table, filling unmatched right-side columns with NULL. Use the tokens provided.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-inner-vs-outer-join** (match): Match each SQL join type to its row-preservation behavior. Assume standard SQL semantics.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-inner-vs-outer-join** (assemble): Assemble the SQL clause that returns all rows from the left table and matching rows from the right table, filling unmatched right-side columns with NULL. Use the tokens below. The clause must be in the order: LEFT, OUTER, JOIN.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-join-vs-subquery** (bucket): Classify each SQL scenario as better expressed with a JOIN or a subquery. Assume standard SQL semantics and that the query needs to return the specified result without unnecessary duplicate rows.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-join-vs-subquery** (order): Order the steps for choosing between a JOIN and a subquery when writing a SQL query, from first consideration to final verification.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-join-vs-subquery** (match): Match each SQL construct to its primary semantic role. Assume standard SQL semantics and a typical optimizer.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-join-vs-subquery** (numeric): Consider a customers table with 1000 rows and an orders table with 5000 rows. Each customer has exactly 5 orders. You run the following query:

SELECT c.id, o.id
FROM customers c
JOIN orders o ON o.customer_id = c.id;

How many rows does this query return?
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-joins** (assemble): Assemble the SQL clause that returns all employees and their department names, including employees with no department. Use the Employees table (columns: id, name, dept_id) and the Departments table (columns: id, dept_name).
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-joins** (assemble): Assemble the SQL clause that returns only rows with a match in both tables, using the standard syntax for an inner join between `employees` and `departments` on `dept_id`.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-joins** (bucket): Classify each SQL join scenario by the join type that best expresses it. Buckets: INNER JOIN, LEFT JOIN, FULL OUTER JOIN, CROSS JOIN. Each scenario belongs to exactly one bucket.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-joins** (assemble): Assemble the SQL clause that returns all rows from both tables, filling unmatched columns with NULL.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-lag-and-lead** (assemble): Assemble the SQL expression that returns the value from the row two positions before the current row, using a default of 0 when no such row exists, within each partition defined by the column `region`, ordered by `event_date`. Use the tokens provided. The expression is a single line of SQL.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-lag-and-lead** (match): Match each SQL window function or clause to its meaning in the context of LAG and LEAD.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-lag-and-lead** (assemble): Assemble the SQL expression that returns the previous row's TotalSales within each Region, ordered by SaleMonth, using a default of 0 when there is no previous row. Tokens may be used once.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-recursive-ctes** (assemble): Assemble the recursive member of a recursive CTE that finds all descendants of a given employee, using the employees table with columns id, name, manager_id. The CTE is named emp_tree and has columns id, name, manager_id, level. The anchor selects the starting employee with id = 1 and level 0. The recursive member should join employees to emp_tree on manager_id = id and increment level by 1. Use UNION ALL to combine the anchor and recursive members. Arrange the tokens to form the recursive member.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-row-number-rank-dense-rank** (grid_toggle): Consider a table `employees` with columns `department`, `name`, and `salary`. For each department, you want to assign a rank to each employee by salary descending, with ties getting the same rank and no gaps in rank values. You also want to assign a unique sequential number to each employee within their department, ordered by salary descending, with ties broken arbitrarily. Which cells correctly describe the behavior of DENSE_RANK() and ROW_NUMBER() in this scenario?
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-row-number-rank-dense-rank** (bucket): Classify each SQL ranking function by its tie-handling behavior. Assume standard SQL semantics with ORDER BY on a column containing duplicate values.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-row-number-rank-dense-rank** (assemble): Assemble the SQL clause that assigns a rank to each row within a partition, giving tied rows the same rank and continuing with the next integer without gaps. Use the tokens below.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-set-operations** (assemble): Assemble the SQL set operation clause that returns distinct rows appearing in both input result sets, using the tokens below. The clause must be syntactically correct.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-set-operations** (match): Match each SQL set operation term to its meaning. Assume standard SQL semantics.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-sql-injection-prevention** (assemble): Assemble the SQL statement that safely looks up a user by username and password using parameterized queries. Assume the database driver uses ? as the placeholder for bound parameters.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-stored-procedures** (match): Match each SQL Server stored procedure term with its correct meaning.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-stored-procedures** (assemble): Assemble the SQL Server statement that creates a stored procedure named usp_UpdateCreditLimit that accepts an integer input parameter @CustomerID and a decimal input parameter @NewLimit, and updates the CreditLimit column of the Customers table for that customer. Use the tokens below.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-stored-procedures** (assemble): Assemble the SQL Server statement that creates a stored procedure named dbo.usp_UpdateCreditLimit that accepts an integer parameter @CustomerID and a decimal parameter @NewLimit, and updates the CreditLimit column of the Customers table for that customer. Use the tokens below. The statement must be syntactically correct and complete.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-subqueries** (match): Match each SQL subquery term to its correct meaning. Assume standard SQL semantics.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-subqueries** (order): Order the steps to correctly write a query that finds employees whose salary is above their department average, using a correlated subquery. Assume standard SQL semantics.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-union-vs-union-all** (assemble): Assemble the SQL clause that removes duplicate rows from the combined result of two query blocks. Use the tokens provided. The clause must be syntactically correct and complete.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-views** (assemble): Assemble the SQL statement that creates a view named vw_active_employees that selects emp_id, name, and dept from employees where is_active = 1, and ensures that any INSERT or UPDATE through the view must satisfy the view's WHERE clause. Use the tokens provided.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-views** (assemble): Assemble the SQL clause that, when added to a view definition, rejects INSERT or UPDATE statements through the view that would produce rows outside the view's WHERE clause. Use all tokens exactly once.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-where-vs-having** (bucket): Classify each SQL predicate by where it belongs in a SELECT query: WHERE or HAVING. Assume standard SQL with strict grouping rules.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-where-vs-having** (assemble): Assemble the SQL clause that filters groups after aggregation, using the tokens below. The clause must reference the aggregate alias `avg_salary` and keep only groups where it exceeds 90000.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-window-functions** (match): Match each window function term to its meaning. Assume standard SQL behavior with ORDER BY present where relevant.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **sql-window-functions** (assemble): Assemble the SQL clause that computes a row-by-row running total of salary within each department, ordered by hire_date. Use the tokens below to form the correct OVER clause for the window function SUM(salary).
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **sql-window-functions** (assemble): Assemble the SQL frame clause that makes a running total count each row individually, including peers, in the order specified by the window's ORDER BY. Use the tokens provided.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **string** (order): Order the steps of the myAtoi parsing algorithm for input "   -0042abc" from first to last.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **trees** (match): Match each tree problem to the traversal or technique that is most appropriate for solving it efficiently.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **two-pointers** (order): Arrange the following steps in the correct order for solving a pair-sum problem on a sorted array using the two-pointer technique. Start with the initial setup and end with the final result.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **two-pointers** (assemble): Assemble the line that moves the left pointer in the two-pointer pair-sum loop on a sorted array when the current sum is below the target. Use all tokens exactly once.
  - Gate said: guessable by elimination: 3/3 samples flagged it

- **two-pointers** (order): Arrange the steps of the two-pointer algorithm for Two Sum II on a sorted array into the correct order, from initialization to returning the answer. Assume the array is sorted in non-decreasing order and the target is given.
  - Gate said: guessable by elimination: 2/3 samples flagged it

- **two-pointers** (match): Match each two-pointer operation to its time complexity, assuming the input is already sorted where required and no extra output storage is counted.
  - Gate said: guessable by elimination: 2/3 samples flagged it
