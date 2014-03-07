MHVDBv2
=======
*(needs a better name)*

The goal of this project is to create a replacement for MHVDB. The system will store the details of members, and transactions to and from the organisation. It will allow users to sign up as members, update their details, and pay money. It will allow admins to create incoming and outgoing transactions, and view reports on members and transactions.

This project uses Flask and Peewee.

Database Design
---------------

- Entities
  - ID *(auto)*
  - Name *(required)*
  - Email Address *(required for members)*
  - Phone number etc *(member info)*
  - Is a member? *(to distinguish members from other things, e.g. ACTPG)*
- Payments
  - ID *(auto)*
  - Date *(required)*
  - Entity ID *(required)*
  - Amount *(required, can be negative for outgoings)*
  - Source *(Bank deposit, Stripe, Bitcoin, etc)*
  - Payment or Contribution? *(to differentiate "I bought $50 of acrylic from MHV, here's the money" from "Here's $50 membership")*
  - Notes/Memo field

Views
-----
 - Sign me up!
 - Update my details *(via one-off link sent to email, or OAuth)*
 - Payment page *(choose amount, choose method, give money)*
 - Admin
   - Create a payment
   - View members
   - View other entities
   - View payments *(filter by entity and date range)*
