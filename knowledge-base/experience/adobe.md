# Work Experience

## Computer Scientist - GenStudio

**Adobe** | March 2025 - Present (1 month)
_San Francisco Bay Area_

### GenStudio Extensibility Framework

**GenStudio** is Adobe's generative AI platform for content automation, enabling users to create marketing and advertising content using AI-driven tools. The platform focuses on automating the content creation process, making it easier for businesses to generate high-quality marketing materials quickly and efficiently.

- Joined the GenStudio team at Adobe to focus on generative AI and content automation
- Working on **extensibility framework** for Adobe's GenStudio, enabling developers to create custom solutions
  - use cases including **claim validation** for generated content for marketing and advertising from GenStudio to make sure the content is valid and adheres to company guidelines
- Immediately onboarded without any training or ramp-up time, demonstrating strong adaptability and quick learning capabilities. Example such as
  - demo bug fixes and enhancements to the extensibility framework on the second day of joining.
  - major contribution to Adobe summit demo features during the initial two weeks of joining.
- Contributed to the development of **Adobe's GenStudio** Create UI in **React**.

## Computer Scientist - AEM Assets as a Cloud Service

**Adobe** | June 2021 - March 2025 (3 years 10 months)
_San Francisco Bay Area_

### Data Services Team - **Dev Lead** (6 months)

AEM Data Services is a data platform team for Adobe Experience Manager (AEM) Assets as a Cloud Service, providing real-time data aggregation and reporting capabilities for AEM product teams and customers. The goal is to enable data-driven decision-making and enhance customer engagement through insights derived from usage metrics.

- **Led a team of five engineers** to develop a **data platform** for an event-driven system on AEM author instances
- Designed and implemented custom **ETL pipelines** using **Golang** and **Circle CI** to aggregate data into a data warehouse such as Snowflake. The data warehouse serves as a source of truth for,
  - reporting and analytics of new AEM pricing and bundling adoptions
  - customer usage and engagement metrics for AEM Assets as a Cloud Service
- Developed **Sling filters** to intercept HTTP events in AEM for real-time user event generation.

### AEM Brand-Aware Tagging with LLM - **Dev Lead** (3 months)

AEM Brand-Aware Tagging with LLM is a proof-of-concept project, which eventually GA, to integrate Adobe Experience Manager (AEM) Assets with Large Language Models (LLM) to enhance asset management capabilities. The goal is to leverage AI to automate metadata generation and improve the tagging process for digital assets.

- **AI-Powered Metadata**: Integrated AEM product tagging with LLM models (GPT-4o, GPT-4o-mini) using vision to generate metadata (tags, titles, descriptions)
- **SKU Extraction with RAG**: Extracted SKUs from images and stored them in a **vector DB for Retrieval-Augmented Generation (RAG)** through **Azure AI Foundry**.
- Map Azure AI services to **Adobe Firefall, Adobe's internal AI platform**, to enable seamless integration with Adobe's ecosystem.
- **Presented LLM capabilities to Adobe's engineering teams and leadership**, showcasing the potential of AI in enhancing AEM asset management capabilities.
- **Led a team of three** to develop a proof-of-concept for the integration of AEM Brand-Aware Tagging with LLM.
  - Using Adobe IO **serverless** platform to deploy the proof-of-concept.
- Provide detailed COGs (cost of goods) analysis for the integration of LLM with AEM Assets, including cost estimates for Azure AI services vision model.
  - This analysis queries AEM Assets Computes serverless platform historical usage data including metadata such as width, height, and file size of images to estimate the cost of running the LLM model on different resolution with high versus low quality parameters.

### AEM Reporting Service - **Distributed System** Dev Lead (6 months) Contributor (1.5 year)

AEM Reporting Service is a distributed system for reporting and analytics on AEM Assets as a Cloud Service. It provides insights into real-time customer usage and engagement metrics, enabling data-driven decision-making for AEM product teams as well as customer reporting needs.

- Joined the AEM Reporting Service team to develop a **distributed system** for reporting and analytics on AEM Assets as a Cloud Service.
- Become a **core maintainer/dev lead** of **five Java Spring Boot microservices** that utilize **Kafka** for **event-driven architecture** to handle reporting APIs.
- Maintain the **Open API documentation** and **Swagger UI** for the reporting service both internally and externally.
- Utilized **Azure Data Explorer (user events), CosmosDB (report schema), and Azure Blob Storage (reports)** for data storage and retrieval.
- Migrated data via **Azure Data Factory** and optimized query performance with materialized views
- Built **React UI** solutions with Adobe's micro-frontend framework for statistical data visualization
- Automated e2e test using **Jenkins**.
- Contribute to performance test framework using **Gatling** to simulate user events and measure the performance of the reporting service under load.
- Led and design the scheduled reporting feature to generate report on a periodic basis e2e:
  - Database schema update to support scheduled reports
  - Separate report creation to new microservice report-consumer to decouple the report generation from the reporting service, and delegate the report generation to the target data warehouse (Azure Data Explorer).
  - Follow the shared-database-per-service pattern to avoid major refactoring which can potentially break existing production feature reporting APIs.
  - Introduce new microservice report-scheduler to schedule the report generation, retry, and monitor report status update.
- Helped cross organization teams to onboard to the AEM Reporting Service by providing documentation and support for their reporting needs.
  - Successfully onboard other teams and add Data Bricks to the list of supported data warehouse for reporting and analytics.
- **Lead the major refactoring** of the reporting service to support cross organization teams contributions.
  - Refactor service to be base on **modulith structure** to support multiple teams contributions and ownership of the reporting service.
- **Work with Principal Engineer** to design and implement **Health Check** and Circuit Breaker for the reporting service to improve the resiliency of the service. Which is used as a template for other AEM microservices.

### Content Automation - **Serverless** OpenWhisk (3 months)

Asset Compute Service is a scalable and extensible service of Adobe Experience Cloud to process digital assets. It can transform image, video, document, and other file formats into different renditions including thumbnails, extracted text and metadata, and archives.

- Contributed to Node.js serverless stack for asset transformation using ImageMagick, ffmpeg, and Azure Media Service

### Indexing Performance - Jackrabbit Oak, MongoDB (6 months)

The challenge about this project is to improve the indexing performance of AEM Assets as a Cloud Service which is based on Jackrabbit Oak and MongoDB, where the Oak repository is a Java content repository with long history and is widely used in AEM.
The success of this project is to improve the indexing performance of AEM Assets as a Cloud Service by 3x, which is a significant improvement for the AEM product.

- Improved indexing speed 3x by transforming a single-process system into a **parallel-processing architecture**
- **Identified performance bottlenecks**, replaced gzip with lz4 compression, and optimized OS settings

### Project Franklin - Vanilla JS, HTML, CSS (2 months)

- Contributed to reimplement RiteAid's Elixir solution website in the Adobe Franklin VIP project using Vanilla JS, HTML, and CSS
- Achieved a perfect 100 Lighthouse score for customer site rewrote (elixirsolutions.com)
