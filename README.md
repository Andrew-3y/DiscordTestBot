# 🚀 DiscordTestBot

A modular, production-ready Discord bot built using `discord.py`, featuring slash commands, PostgreSQL persistence, and cloud deployment via Railway.

This project treats a Discord bot as a backend system rather than a simple command script. It is designed with clean architecture principles, asynchronous programming patterns, and scalable data modeling in mind.


## 🧠 Architecture Overview

The bot follows a modular cog-based architecture using `discord.py`, where each feature is isolated into its own component to maintain separation of concerns and improve maintainability.

Core architectural decisions:

- Event-driven interaction handling  
- Slash command–based interface (modern Discord standard)  
- Asynchronous PostgreSQL integration via `asyncpg`  
- Connection pooling for non-blocking database operations  
- Composite primary key modeling to guarantee per-guild data isolation  
- Conflict-safe upserts using `ON CONFLICT DO UPDATE`  
- Environment-based configuration (no hardcoded secrets)  
- Cloud-native deployment via Railway with automatic redeployment  

This structure ensures the bot remains scalable, secure, and easy to extend.


## ⚙️ Core Features

- Slash command system (`/`)
- Server approval system
- PostgreSQL-backed persistent storage
- Poll system using Discord interaction components
- Owner-restricted administrative commands
- Multi-server data isolation
- Automatic deployment through GitHub integration


## 🗄 Database Design

The bot uses PostgreSQL for persistent state management.

Design principles:

- Composite primary keys for per-guild isolation  
- Safe upsert operations to prevent duplicate records  
- Asynchronous query execution for performance  
- Persistent approval state tracking  

This enables reliable operation across multiple servers without data conflicts.


## 🔐 Required Environment Variables

The bot requires the following environment variables:

TOKEN=your_discord_bot_token

DATABASE_URL=your_postgresql_connection_string

OWNER_ID=your_discord_user_id

Environment variables are used to ensure secure credential management and production portability.


## ☁️ Deployment

The bot is deployed using Railway as a persistent worker process.  
GitHub integration allows automatic redeployment on push, supporting a clean CI/CD workflow.


## 🧠 Design Philosophy

This project emphasizes:

- Separation of concerns  
- Asynchronous non-blocking execution  
- Persistent multi-guild data modeling  
- Safe database concurrency handling  
- Modular extensibility  
- Cloud-native deployment patterns  

The goal is to build Discord applications using real backend engineering principles.


## 📚 Technology Stack

- Python  
- discord.py  
- asyncpg  
- PostgreSQL  
- Railway  
- GitHub (CI/CD integration)  
