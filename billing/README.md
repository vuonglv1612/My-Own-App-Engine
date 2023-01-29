# Usage-Based Billing System

This is a simple usage-based billing system. It is designed to be used by a single tenant, and is not intended to be
used by multiple tenants.

## Overview

// TODO: Talk about the system

## Architecture

// TODO: Talk about the architecture

## Getting Started

### Prerequisites

### Installation

### Migration Database

```bash
sudo apt-get install libpq-dev python3-dev
poetry install --with migration
```

#### Create New Revision

```bash
poetry run alembic -c infrastructure/postgres/migration/alembic.ini revision --autogenerate --rev-id 002 -m "Added Product"
```

#### Upgrade Database

```bash
poetry run alembic -c infrastructure/postgres/migration/alembic.ini upgrade head
```

### Usage

