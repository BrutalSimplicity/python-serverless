# Overview

This library includes a set of tools for creating cloud applications in Python 3. It attempts to codify some best practices around common concerns when building cloud applications. 

!!! note "Express Yourself!"
    The library opts for expressiveness of code over other factors like performance, as many cloud applications should handle these concerns through the cloud services provided and allow business logic to reveal its intent as clearly as possible.

## Features
- **Structured Logging.** Add structured logging to cloudwatch using a simple function decorator
- **Build expressive data pipelines.** Manipulate data streams and build workflows using a common set of collection operations (i.e. similar to Javascript Lodash, Java Streams, or .Net Linq)
- **Adopt event-driven architecture.** Build event-driven systems using the Event Bridge and SNS function decorators
- **Optional handling.** Simplify unknown object retrieval using optional path handling
- **Paginate Dynamodb queries.** Easily paginate Dynamodb queries using the basic `for` loop
- **Lazy Evaluation.** Lazily resolve values on access to ease testing and reduce unecessary overhead
- **Request Caching.** Cache data throughout a single request to prevent redunant data fetches and simplify data access patterns
- **Lots more.** Many other data utilities... Read through the guide to learn more.

## Install

This library can be installed with your favorite dependency management tool.
