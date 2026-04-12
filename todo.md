# High-Level Implementation Plan for the Multimodal Orthopaedic RAG System

## [x] Phase 1: Project Initialization & Infrastructure

Set up the project foundation, development environments, and service boundaries.

* [x] Create the monorepo structure for backend, frontend, shared protobuf contracts, and deployment configs.
* [x] Configure Docker-based local development for all services.
* [x] Define and compile the initial gRPC Protocol Buffer contracts.
* [x] Establish environment-variable management for API keys, model settings, and database connections.
* [x] Add initial project scripts for local development, container startup, and protobuf regeneration.
* [ ] Add centralized config loading and validation for all services.
* [ ] Add basic CI checks for formatting, linting, protobuf generation, and build verification.
* [ ] Define service boundaries clearly:

  * vision extraction service
  * retrieval service
  * orchestration service
  * frontend gateway

---

## [x] Phase 2: The Vision Extraction Engine

Build the multimodal pipeline that receives orthopaedic imaging, sends it to the vision model, and returns structured radiographic findings.

* [x] Build the Go pipeline to accept streamed image chunks over gRPC.
* [x] Reconstruct the uploaded image from the incoming byte stream.
* [x] Pass the image and optional clinical history to the multimodal vision model.
* [x] Securely query the external Vision-Language Model for radiographic findings.
* [x] Return model output to the backend pipeline.

### Extend this phase with:

* [ ] Replace base64 as the default transport step with **raw byte handling** for the SDK path.
* [ ] Validate image type, size, and format before sending to the model.
* [ ] Add structured output generation using a strict JSON schema.
* [ ] Add Go-side schema validation and unmarshalling into typed structs.
* [ ] Standardize the response format for:

  * diagnosis
  * bone name
  * findings
  * classification
  * uncertainty / limitations
* [ ] Add support for multiple image views later:

  * AP
  * lateral
  * oblique
* [ ] Add robust model request handling:

  * timeouts
  * retries
  * transient error handling
  * invalid JSON handling
* [ ] Add provider abstraction so the system can swap models later without changing business logic.

---

## Phase 3: Vector Database & Knowledge Ingestion

Deploy the retrieval layer and prepare the orthopaedic knowledge base for semantic search.

* [ ] Choose the vector store for v1:

  * Qdrant for dedicated vector search
  * or pgvector if you want simpler operational consolidation
* [ ] Deploy the vector database locally with Docker.
* [ ] Define the document schema for stored knowledge chunks.
* [ ] Write the ingestion pipeline to:

  * load FRCS / orthopaedic notes
  * clean and normalize the content
  * split into semantically useful chunks
  * generate embeddings
  * store vectors with metadata
* [ ] Attach useful metadata to each chunk:

  * topic
  * anatomical region
  * fracture type
  * source
  * chapter / page
  * confidence / quality label
* [ ] Build re-ingestion support so updated notes can be reprocessed safely.
* [ ] Add source-version tracking for knowledge updates.
* [ ] Add a small seed dataset for early testing before full ingestion.

---

## Phase 4: Semantic Retrieval & LLM Synthesis

Use the vision output to retrieve relevant orthopaedic knowledge and synthesize a grounded answer.

* [ ] Convert the structured vision output into one or more retrieval queries.
* [ ] Implement similarity search against the vector database.
* [ ] Add metadata filtering to improve relevance, such as:

  * bone
  * joint
  * fracture classification
  * trauma type
* [ ] Rank and re-rank retrieved chunks before final prompt construction.
* [ ] Build the final grounded prompt using:

  * structured vision findings
  * clinical history
  * retrieved orthopaedic references
* [ ] Generate the final evidence-grounded synthesis.

### Define the v1 output clearly:

* [ ] Structured radiographic summary
* [ ] Retrieved supporting references
* [ ] Grounded management / learning guidance
* [ ] Explicit uncertainty statement when evidence is weak

### Add quality controls:

* [ ] Add citation mapping from generated response back to retrieved chunks.
* [ ] Add hallucination reduction rules in prompt construction.
* [ ] Add retrieval evaluation on test cases.
* [ ] Add answer evaluation for factual grounding and clinical consistency.

---

## Phase 5: The gRPC Orchestrator Server

Complete the backend orchestration flow and expose the end-to-end clinical pipeline.

* [ ] Finalize the Go server logic for the full pipeline:

  * receive image stream
  * call vision extraction
  * retrieve relevant knowledge
  * generate grounded response
  * stream results back to the client
* [ ] Define clear internal interfaces between components.
* [ ] Add streaming status events for the client, such as:

  * upload received
  * image processed
  * retrieval in progress
  * synthesis in progress
  * final response ready
* [ ] Add request-scoped logging and correlation IDs.
* [ ] Add timeout policies for each step.
* [ ] Add graceful failure messages for:

  * invalid image
  * model timeout
  * no relevant retrieval hits
  * malformed model output
* [ ] Add fallback behavior if one model/provider fails.
* [ ] Add unit and integration tests for the orchestration flow.

---

## Phase 6: The Clinical Frontend Interface

Build the clinician-facing interface for uploading images and viewing structured grounded reports.

* [ ] Build the Vue dashboard with Envoy proxy integration.
* [ ] Add drag-and-drop X-ray upload.
* [ ] Add clinical-history input field.
* [ ] Build the structured report UI for:

  * diagnosis
  * findings
  * classification
  * retrieved evidence
  * recommendations / summary
* [ ] Add live streaming UI for backend progress updates.
* [ ] Add loading, retry, and failure states.
* [ ] Add case history panel so users can review prior runs locally.
* [ ] Add a clean layout for side-by-side display:

  * uploaded image
  * model findings
  * retrieved orthopaedic knowledge
* [ ] Add a clinician note / override section for manual interpretation.

---

## Phase 7: Safety, Evaluation, and Governance

Make the system safer, testable, and usable in a clinical-learning context.

* [ ] Define the system scope clearly:

  * educational support
  * decision support
  * not autonomous diagnosis
* [ ] Add uncertainty handling in the output contract.
* [ ] Build a benchmark dataset of labelled orthopaedic X-ray cases.
* [ ] Evaluate:

  * structured extraction quality
  * retrieval relevance
  * grounding accuracy
  * consistency of final output
* [ ] Add manual review workflows for difficult or low-confidence cases.
* [ ] Add audit logs for model requests and outputs.
* [ ] Add de-identification checks for uploaded cases.
* [ ] Add secret handling and secure storage rules for all API credentials.

---

## Phase 8: Deployment, Monitoring, and Scaling

Prepare the system for reliable real-world usage.

* [ ] Containerize all services for reproducible deployment.
* [ ] Add production-ready Envoy routing.
* [ ] Add metrics and monitoring for:

  * request latency
  * model latency
  * retrieval latency
  * failure rates
  * token / API usage
* [ ] Add structured logs and tracing.
* [ ] Add health checks for backend services.
* [ ] Add backup / restore strategy for the vector database.
* [ ] Add cost monitoring for external model usage.
* [ ] Plan for future support of:

  * DICOM ingestion
  * multi-image studies
  * on-prem / self-hosted model options

---

# Tech Stack

* **Backend:** Go, gRPC
* **Gateway / Proxy:** Envoy
* **Frontend:** Vue
* **Vector DB:** Qdrant or pgvector
* **Containerization:** Docker
* **LLM / Vision Layer:** Gemini multimodal API
* **Embedding / Retrieval Layer:** TBD based on benchmark results

---

# Immediate Next Priorities

* [ ] Finalize the structured output schema for the vision model
* [ ] Complete typed parsing and validation in Go
* [ ] Stand up the vector database locally
* [ ] Ingest the first orthopaedic note set
* [ ] Connect vision output to semantic retrieval
* [ ] Define the final grounded response contract

If you want this turned into a cleaner **GitHub-style `TODO.md`** with nested checkboxes and priorities, say **“format it as a project TODO file”**.
