#!/usr/bin/env python3
"""
TuskLang Python CLI - AI Commands
=================================
AI-powered operations and integrations
"""

import os
import json
import requests
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path

from ..utils import output_formatter, error_handler, config_loader


class AIConfig:
    """AI configuration management"""
    
    def __init__(self):
        self.config_file = Path.home() / '.tsk' / 'ai_config.json'
        self.config_file.parent.mkdir(exist_ok=True)
        self.load_config()
    
    def load_config(self):
        """Load AI configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}
        else:
            self.config = {}
    
    def save_config(self):
        """Save AI configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for service"""
        return self.config.get(f'{service}_api_key')
    
    def set_api_key(self, service: str, key: str):
        """Set API key for service"""
        self.config[f'{service}_api_key'] = key
        self.save_config()


class AIService:
    """Base AI service class"""
    
    def __init__(self, config: AIConfig):
        self.config = config
    
    def query(self, prompt: str) -> Dict[str, Any]:
        """Query AI service - to be implemented by subclasses"""
        raise NotImplementedError


class ClaudeService(AIService):
    """Claude AI service integration"""
    
    def query(self, prompt: str) -> Dict[str, Any]:
        """Query Claude AI"""
        api_key = self.config.get_api_key('claude')
        if not api_key:
            return {'error': 'Claude API key not configured. Run: tsk ai setup'}
        
        try:
            headers = {
                'x-api-key': api_key,
                'content-type': 'application/json',
                'anthropic-version': '2023-06-01'
            }
            
            data = {
                'model': 'claude-3-sonnet-20240229',
                'max_tokens': 4000,
                'messages': [{'role': 'user', 'content': prompt}]
            }
            
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'response': result['content'][0]['text'],
                    'model': result['model'],
                    'usage': result.get('usage', {})
                }
            else:
                return {
                    'error': f'Claude API error: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {'error': f'Claude API request failed: {str(e)}'}


class ChatGPTService(AIService):
    """ChatGPT service integration"""
    
    def query(self, prompt: str) -> Dict[str, Any]:
        """Query ChatGPT"""
        api_key = self.config.get_api_key('chatgpt')
        if not api_key:
            return {'error': 'ChatGPT API key not configured. Run: tsk ai setup'}
        
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-4',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 4000,
                'temperature': 0.7
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'response': result['choices'][0]['message']['content'],
                    'model': result['model'],
                    'usage': result.get('usage', {})
                }
            else:
                return {
                    'error': f'ChatGPT API error: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {'error': f'ChatGPT API request failed: {str(e)}'}


class CustomAIService(AIService):
    """Custom AI API service"""
    
    def __init__(self, config: AIConfig, api_endpoint: str):
        super().__init__(config)
        self.api_endpoint = api_endpoint
    
    def query(self, prompt: str) -> Dict[str, Any]:
        """Query custom AI API"""
        try:
            data = {'prompt': prompt}
            
            response = requests.post(
                self.api_endpoint,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'response': result.get('response', result.get('text', str(result))),
                    'api': self.api_endpoint
                }
            else:
                return {
                    'error': f'Custom API error: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {'error': f'Custom API request failed: {str(e)}'}


def handle_ai_command(args, cli):
    """Handle AI commands"""
    config = AIConfig()
    
    if args.ai_command == 'claude':
        return handle_claude_command(args, cli, config)
    elif args.ai_command == 'chatgpt':
        return handle_chatgpt_command(args, cli, config)
    elif args.ai_command == 'custom':
        return handle_custom_command(args, cli, config)
    elif args.ai_command == 'config':
        return handle_config_command(args, cli, config)
    elif args.ai_command == 'setup':
        return handle_setup_command(args, cli, config)
    elif args.ai_command == 'test':
        return handle_test_command(args, cli, config)
    elif args.ai_command == 'complete':
        return handle_complete_command(args, cli, config)
    elif args.ai_command == 'analyze':
        return handle_analyze_command(args, cli, config)
    elif args.ai_command == 'optimize':
        return handle_optimize_command(args, cli, config)
    elif args.ai_command == 'security':
        return handle_security_command(args, cli, config)
    else:
        output_formatter.print_error("Unknown AI command")
        return 1


def handle_claude_command(args, cli, config):
    """Handle Claude AI command"""
    service = ClaudeService(config)
    result = service.query(args.prompt)
    
    if cli.json_output:
        output_formatter.print_json(result)
    else:
        if result.get('success'):
            print(f"\n🤖 Claude Response:\n")
            print(result['response'])
            if result.get('usage'):
                print(f"\n📊 Usage: {result['usage']}")
        else:
            output_formatter.print_error(result['error'])
            return 1
    
    return 0


def handle_chatgpt_command(args, cli, config):
    """Handle ChatGPT command"""
    service = ChatGPTService(config)
    result = service.query(args.prompt)
    
    if cli.json_output:
        output_formatter.print_json(result)
    else:
        if result.get('success'):
            print(f"\n🤖 ChatGPT Response:\n")
            print(result['response'])
            if result.get('usage'):
                print(f"\n📊 Usage: {result['usage']}")
        else:
            output_formatter.print_error(result['error'])
            return 1
    
    return 0


def handle_custom_command(args, cli, config):
    """Handle custom AI command"""
    service = CustomAIService(config, args.api)
    result = service.query(args.prompt)
    
    if cli.json_output:
        output_formatter.print_json(result)
    else:
        if result.get('success'):
            print(f"\n🤖 Custom AI Response:\n")
            print(result['response'])
        else:
            output_formatter.print_error(result['error'])
            return 1
    
    return 0


def handle_config_command(args, cli, config):
    """Handle AI config command"""
    if cli.json_output:
        output_formatter.print_json(config.config)
    else:
        print("🤖 AI Configuration:")
        print(f"  Config file: {config.config_file}")
        print("\nConfigured services:")
        for key, value in config.config.items():
            if key.endswith('_api_key'):
                service = key.replace('_api_key', '').title()
                status = "✅ Configured" if value else "❌ Not configured"
                print(f"  {service}: {status}")
    
    return 0


def handle_setup_command(args, cli, config):
    """Handle AI setup command"""
    print("🤖 AI Service Setup")
    print("===================")
    
    # Claude setup
    print("\n1. Claude AI Setup:")
    claude_key = input("Enter Claude API key (or press Enter to skip): ").strip()
    if claude_key:
        config.set_api_key('claude', claude_key)
        print("✅ Claude API key configured")
    
    # ChatGPT setup
    print("\n2. ChatGPT Setup:")
    chatgpt_key = input("Enter ChatGPT API key (or press Enter to skip): ").strip()
    if chatgpt_key:
        config.set_api_key('chatgpt', chatgpt_key)
        print("✅ ChatGPT API key configured")
    
    print("\n🎉 AI setup complete!")
    return 0


def handle_test_command(args, cli, config):
    """Handle AI test command"""
    print("🤖 Testing AI Connections...")
    
    results = {}
    
    # Test Claude
    claude_key = config.get_api_key('claude')
    if claude_key:
        service = ClaudeService(config)
        result = service.query("Hello! Please respond with 'Claude is working' if you can see this.")
        results['claude'] = result.get('success', False)
        print(f"Claude: {'✅ Working' if results['claude'] else '❌ Failed'}")
    else:
        results['claude'] = False
        print("Claude: ❌ Not configured")
    
    # Test ChatGPT
    chatgpt_key = config.get_api_key('chatgpt')
    if chatgpt_key:
        service = ChatGPTService(config)
        result = service.query("Hello! Please respond with 'ChatGPT is working' if you can see this.")
        results['chatgpt'] = result.get('success', False)
        print(f"ChatGPT: {'✅ Working' if results['chatgpt'] else '❌ Failed'}")
    else:
        results['chatgpt'] = False
        print("ChatGPT: ❌ Not configured")
    
    if cli.json_output:
        output_formatter.print_json(results)
    
    return 0


def handle_complete_command(args, cli, config):
    """Handle AI completion command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Get context around cursor position
    lines = content.split('\n')
    line_num = args.line or len(lines)
    column_num = args.column or len(lines[line_num - 1]) if line_num <= len(lines) else 0
    
    # Create completion prompt
    context = '\n'.join(lines[:line_num])
    prompt = f"""Complete the following TuskLang code at line {line_num}, column {column_num}:

{context}

Please provide a completion that follows TuskLang syntax and best practices."""

    # Use Claude for completion
    service = ClaudeService(config)
    result = service.query(prompt)
    
    if cli.json_output:
        output_formatter.print_json(result)
    else:
        if result.get('success'):
            print(f"\n🤖 AI Completion for {args.file}:{line_num}:{column_num}\n")
            print(result['response'])
        else:
            output_formatter.print_error(result['error'])
            return 1
    
    return 0


def handle_analyze_command(args, cli, config):
    """Handle AI analysis command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Create analysis prompt
    prompt = f"""Analyze the following TuskLang code for errors, improvements, and best practices:

{content}

Please provide:
1. Any syntax errors or issues
2. Performance improvements
3. Security considerations
4. Code style suggestions
5. Best practices recommendations"""

    # Use Claude for analysis
    service = ClaudeService(config)
    result = service.query(prompt)
    
    if cli.json_output:
        output_formatter.print_json(result)
    else:
        if result.get('success'):
            print(f"\n🔍 AI Analysis for {args.file}:\n")
            print(result['response'])
        else:
            output_formatter.print_error(result['error'])
            return 1
    
    return 0


def handle_optimize_command(args, cli, config):
    """Handle AI optimization command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Create optimization prompt
    prompt = f"""Analyze the following TuskLang code for performance optimization opportunities:

{content}

Please provide specific optimization suggestions including:
1. Algorithm improvements
2. Memory usage optimizations
3. Caching strategies
4. Database query optimizations
5. Code structure improvements"""

    # Use Claude for optimization
    service = ClaudeService(config)
    result = service.query(prompt)
    
    if cli.json_output:
        output_formatter.print_json(result)
    else:
        if result.get('success'):
            print(f"\n⚡ AI Performance Optimization for {args.file}:\n")
            print(result['response'])
        else:
            output_formatter.print_error(result['error'])
            return 1
    
    return 0


def handle_security_command(args, cli, config):
    """Handle AI security command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Create security analysis prompt
    prompt = f"""Analyze the following TuskLang code for security vulnerabilities:

{content}

Please identify:
1. SQL injection vulnerabilities
2. XSS vulnerabilities
3. Authentication/authorization issues
4. Input validation problems
5. Sensitive data exposure
6. Security best practices violations
7. Recommendations for fixes"""

    # Use Claude for security analysis
    service = ClaudeService(config)
    result = service.query(prompt)
    
    if cli.json_output:
        output_formatter.print_json(result)
    else:
        if result.get('success'):
            print(f"\n🔒 AI Security Analysis for {args.file}:\n")
            print(result['response'])
        else:
            output_formatter.print_error(result['error'])
            return 1
    
    return 0 