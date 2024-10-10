# auto-tco

Using Document AI API and custom processor with schema fields I defined to extract structured data from Cloud invoices, starting with Amazon Web Services invoices. 

F1 Score of current processor is 0.943. It extracts all schema fields with a 1.0 confidence level, aside from occassionally missing Invoice IDs (because some invoices do not contain them, or contain a template string as its not been exported correctly - data issue).

Attempted two approaches:

1. Local file analysis. Sent to deployed custom processor. File is processed and extracted data returned accrording to schema fields. You can see the data returned in XLSX and CSV files. There is a contexutal issue as line items, usage and pricing are pulled out individually. To improve this process, a new model would need to be trained using this format with a good F1 score achieved e.g. labelling box that encompasses line item, usage and pricing in a single box so line_item returns item, usage and price as a single data point. Another issue with this dataset is the information contained in an invoice does not always include everything you'd need to perform a precise cost assessment (as there are different methods of exporting / architectures / ways where its hard to capture the usage). 


2. Second approach is a basic frontend. File uploaded by user. File stored in cloud storage bucket. File sent from bucket to custom Doc AI processor, extracted data returns document.text. Entire document.text is used alongside a prompt to perform a detailed cost assessment to gemini-1.5-flash-002. Output is tidied up to remove weird syntax and the analysis is displayed. The cost assessment analysis does often include disclaimers - like not based on latest pricing data (2023 data etc.), even if asked to exclude disclaimers in the prompt. It does seem to understand the context of the invoice from the document.text, despite the line item, price and usage being separate items as explained above. Not able to get this model to perform an analysis and display as structured data for a CSV/XLSx file. 

Budget: $140.47/$500

Doc AI API has now been disabled.
There are Quota issues - resource exhausted that's not displaying in the billing/quotas section - unsure on Quota issue but may be the amount of text (min. 450 line items) being run through the model.