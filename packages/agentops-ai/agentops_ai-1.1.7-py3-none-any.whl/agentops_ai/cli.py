"""
AgentOps CLI - AI-powered QA co-pilot for requirements-driven test automation.
"""

import click
import os
import sys
from typing import List, Optional
from .agentops_core.workflow import AgentOpsWorkflow
from .agentops_core.requirements_clarification import RequirementsClarificationEngine
from .agentops_core.language_support import get_language_manager, LanguageType, detect_language


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """AgentOps - AI-powered QA co-pilot for requirements-driven test automation."""
    pass


@cli.command()
@click.argument('source_files', nargs=-1)
@click.option('--approval-mode', '-a', default='fast', 
              type=click.Choice(['fast', 'manual', 'auto']),
              help='Approval mode for requirements')
def run(source_files, approval_mode):
    """Run the complete AgentOps workflow on source files."""
    if not source_files:
        click.echo("❌ No source files specified")
        return
    
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.run_multi_agent_workflow(list(source_files), approval_mode)
        
        if result["success"]:
            click.echo("✅ Workflow completed successfully!")
            click.echo(f"📊 Requirements processed: {result.get('requirements_processed', 0)}")
            click.echo(f"🧪 Tests generated: {len(result.get('tests_generated', []))}")
            click.echo(f"📋 Traceability matrix: {result.get('traceability_file', 'N/A')}")
        else:
            click.echo(f"❌ Workflow failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.argument('source_files', nargs=-1)
def extract_requirements(source_files):
    """Extract requirements from source files."""
    if not source_files:
        click.echo("❌ No source files specified")
        return
    
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.extract_requirements_from_files(list(source_files))
        
        if result["success"]:
            click.echo("✅ Requirements extracted successfully!")
            click.echo(f"📊 Requirements found: {result.get('requirements_count', 0)}")
        else:
            click.echo(f"❌ Failed to extract requirements: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.argument('source_files', nargs=-1)
def generate_tests(source_files):
    """Generate tests from requirements."""
    if not source_files:
        click.echo("❌ No source files specified")
        return
    
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.generate_tests_from_files(list(source_files))
        
        if result["success"]:
            click.echo("✅ Tests generated successfully!")
            click.echo(f"🧪 Test files created: {result.get('test_files_created', 0)}")
        else:
            click.echo(f"❌ Failed to generate tests: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
def run_tests():
    """Run all generated tests."""
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.run_all_tests()
        
        if result["success"]:
            click.echo("✅ Tests completed!")
            click.echo(f"📊 Tests run: {result.get('tests_run', 0)}")
            click.echo(f"✅ Passed: {result.get('passed', 0)}")
            click.echo(f"❌ Failed: {result.get('failed', 0)}")
        else:
            click.echo(f"❌ Test execution failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.option('--format', '-f', default='markdown',
              type=click.Choice(['markdown', 'html', 'json']),
              help='Output format for traceability matrix')
def traceability(format):
    """Generate traceability matrix."""
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.generate_traceability_matrix(format)
        
        if result["success"]:
            click.echo("✅ Traceability matrix generated!")
            click.echo(f"📄 Output file: {result.get('file_path', 'N/A')}")
        else:
            click.echo(f"❌ Failed to generate traceability matrix: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.option('--format', '-f', default='gherkin',
              type=click.Choice(['gherkin', 'markdown']),
              help='Export format for requirements')
def export_requirements(format):
    """Export requirements to file."""
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.export_requirements(format)
        
        if result["success"]:
            click.echo("✅ Requirements exported successfully!")
            click.echo(f"📄 Output file: {result.get('file_path', 'N/A')}")
        else:
            click.echo(f"❌ Failed to export requirements: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.argument('requirement_id')
@click.argument('clarification')
@click.option('--method', '-m', default='manual',
              type=click.Choice(['manual', 'auto']),
              help='Update method for clarification')
def clarify_requirement(requirement_id, clarification, method):
    """Clarify a specific requirement."""
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.clarify_requirements(requirement_id, clarification, method)
        
        if result["success"]:
            click.echo("✅ Requirement clarified successfully!")
            click.echo(f"🆔 Requirement ID: {requirement_id}")
            click.echo(f"📝 Clarification: {clarification}")
        else:
            click.echo(f"❌ Failed to clarify requirement: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
def analyze_failures():
    """Analyze test failures and suggest clarifications."""
    try:
        engine = RequirementsClarificationEngine()
        
        # Run pytest to get output for analysis
        import subprocess
        try:
            result = subprocess.run(['python', '-m', 'pytest', '--tb=short'], 
                                  capture_output=True, text=True, cwd='.')
            pytest_output = result.stdout + result.stderr
            failures = engine.analyze_test_failures(pytest_output)
            
            click.echo("✅ Failure analysis completed!")
            click.echo(f"🔍 Failures analyzed: {len(failures)}")
            
            if failures:
                gaps = engine.identify_requirements_gaps(failures)
                click.echo(f"💡 Requirements gaps identified: {len(gaps)}")
                
                for gap in gaps:
                    click.echo(f"  - {gap.suggested_clarification}")
            else:
                click.echo("No test failures found to analyze")
                
        except Exception as e:
            click.echo(f"Error running tests: {e}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
def audit_history():
    """Show requirements clarification audit history."""
    try:
        engine = RequirementsClarificationEngine()
        audits = engine.get_audit_history()
        
        if audits:
            click.echo("📋 Requirements Clarification Audit History")
            click.echo("=" * 60)
            
            for audit in audits:
                click.echo(f"🆔 {audit.audit_id}")
                click.echo(f"📝 Requirement: {audit.requirement_id}")
                click.echo(f"🔧 Method: {audit.update_method}")
                click.echo(f"📅 Timestamp: {audit.timestamp}")
                click.echo(f"💡 Reason: {audit.clarification_reason}")
                click.echo("-" * 40)
        else:
            click.echo("📋 No audit history found")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


# Language Support Commands

@cli.command()
@click.argument('file_path')
def detect_language_cmd(file_path):
    """Detect the programming language of a file."""
    try:
        language = detect_language(file_path)
        if language:
            click.echo(f"🔍 Detected language: {language.value}")
            click.echo(f"📁 File: {file_path}")
        else:
            click.echo(f"❓ Unknown or unsupported language for: {file_path}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.argument('directory', default='.')
def scan_languages(directory):
    """Scan a directory and detect all programming languages present."""
    try:
        from pathlib import Path
        import glob
        
        language_manager = get_language_manager()
        language_counts = {}
        total_files = 0
        
        # Scan for common file extensions
        extensions = ['.py', '.js', '.ts', '.java', '.cs', '.go', '.rs', '.cpp', '.c', '.php', '.rb']
        
        for ext in extensions:
            pattern = f"{directory}/**/*{ext}"
            files = glob.glob(pattern, recursive=True)
            
            for file_path in files:
                language = detect_language(file_path)
                if language:
                    language_counts[language.value] = language_counts.get(language.value, 0) + 1
                    total_files += 1
        
        if language_counts:
            click.echo("🔍 Language Detection Results:")
            click.echo("=" * 40)
            for lang, count in sorted(language_counts.items()):
                click.echo(f"📊 {lang}: {count} files")
            click.echo(f"📁 Total files analyzed: {total_files}")
        else:
            click.echo("📁 No supported language files found")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
def list_supported_languages():
    """List all supported programming languages."""
    try:
        language_manager = get_language_manager()
        languages = language_manager.get_supported_languages()
        
        click.echo("🌐 Supported Programming Languages:")
        click.echo("=" * 40)
        
        for lang in languages:
            analyzer = language_manager.get_analyzer(lang)
            status = "✅ Full Support" if lang == LanguageType.PYTHON else "🟡 Beta Support"
            click.echo(f"📝 {lang.value.title()}: {status}")
            
        click.echo(f"\n📊 Total supported languages: {len(languages)}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.argument('language')
@click.option('--enable/--disable', default=True, help='Enable or disable language support')
def configure_language(language, enable):
    """Configure language support for a specific language."""
    try:
        language_manager = get_language_manager()
        
        # Convert string to LanguageType enum
        try:
            lang_type = LanguageType(language.lower())
        except ValueError:
            click.echo(f"❌ Unsupported language: {language}")
            click.echo("💡 Use 'list-supported-languages' to see available options")
            return
        
        if enable:
            success = language_manager.enable_language(lang_type)
            if success:
                click.echo(f"✅ Enabled {language} support")
            else:
                click.echo(f"❌ Failed to enable {language} support")
        else:
            success = language_manager.disable_language(lang_type)
            if success:
                click.echo(f"✅ Disabled {language} support")
            else:
                click.echo(f"❌ Failed to disable {language} support")
                
    except Exception as e:
        click.echo(f"❌ Error: {e}")


# Enhanced Test Running Commands

@cli.command()
@click.argument('repository_path', default='.')
@click.option('--level', '-l', type=int, default=1, help='Test complexity level (1-5)')
@click.option('--language', '-lang', help='Specific language to test')
@click.option('--parallel', '-p', is_flag=True, help='Run tests in parallel')
@click.option('--report', '-r', is_flag=True, help='Generate detailed report')
def run_comprehensive_tests(repository_path, level, language, parallel, report):
    """Run comprehensive tests on a repository with multi-language support."""
    try:
        from tests.comprehensive_test_runner import ComprehensiveTestRunner
        
        runner = ComprehensiveTestRunner()
        
        # Filter repositories by level and language if specified
        test_repos = [repo for repo in runner.test_repos if repo.level == level]
        if language:
            test_repos = [repo for repo in test_repos if repo.language == language.lower()]
        
        if not test_repos:
            click.echo(f"❌ No test repositories found for level {level}")
            if language:
                click.echo(f"   and language {language}")
            return
        
        click.echo(f"🧪 Running comprehensive tests (Level {level})")
        click.echo(f"📁 Repository: {repository_path}")
        click.echo(f"🔧 Parallel execution: {'Yes' if parallel else 'No'}")
        
        if parallel:
            results = runner.run_parallel_tests([level])
        else:
            results = []
            for repo in test_repos:
                result = runner.run_test(repo)
                results.append(result)
        
        # Display results
        passed = sum(1 for r in results if r.status == "PASS")
        failed = sum(1 for r in results if r.status == "FAIL")
        skipped = sum(1 for r in results if r.status == "SKIP")
        
        click.echo(f"\n📊 Test Results:")
        click.echo(f"✅ Passed: {passed}")
        click.echo(f"❌ Failed: {failed}")
        click.echo(f"⏭️ Skipped: {skipped}")
        click.echo(f"📁 Total: {len(results)}")
        
        if report:
            report_content = runner.generate_report()
            report_file = f"comprehensive_test_report_{level}.md"
            with open(report_file, 'w') as f:
                f.write(report_content)
            click.echo(f"📄 Detailed report saved to: {report_file}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.argument('repository_path', default='.')
@click.option('--complexity', '-c', type=click.Choice(['simple', 'medium', 'complex']), 
              help='Repository complexity level')
@click.option('--structure', '-s', type=click.Choice(['flat', 'nested', 'monorepo', 'microservices']),
              help='Repository structure type')
def analyze_repository_structure(repository_path, complexity, structure):
    """Analyze repository structure and complexity."""
    try:
        from pathlib import Path
        import json
        
        repo_path = Path(repository_path)
        if not repo_path.exists():
            click.echo(f"❌ Repository path does not exist: {repository_path}")
            return
        
        # Analyze structure
        analysis = {
            "path": str(repo_path),
            "total_files": 0,
            "languages": {},
            "structure": "unknown",
            "complexity": "unknown",
            "dependencies": [],
            "build_systems": []
        }
        
        # Count files and detect languages
        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                analysis["total_files"] += 1
                
                # Detect language
                language = detect_language(str(file_path))
                if language:
                    analysis["languages"][language.value] = analysis["languages"].get(language.value, 0) + 1
                
                # Detect build systems
                if file_path.name in ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle', 
                                    'Cargo.toml', 'go.mod', '*.csproj', 'Makefile']:
                    analysis["build_systems"].append(file_path.name)
        
        # Determine structure type
        if (repo_path / "packages").exists() or (repo_path / "services").exists():
            analysis["structure"] = "monorepo"
        elif (repo_path / "src").exists() and (repo_path / "tests").exists():
            analysis["structure"] = "nested"
        else:
            analysis["structure"] = "flat"
        
        # Determine complexity
        if analysis["total_files"] > 1000:
            analysis["complexity"] = "complex"
        elif analysis["total_files"] > 100:
            analysis["complexity"] = "medium"
        else:
            analysis["complexity"] = "simple"
        
        # Display results
        click.echo("🔍 Repository Structure Analysis:")
        click.echo("=" * 50)
        click.echo(f"📁 Path: {analysis['path']}")
        click.echo(f"📊 Total files: {analysis['total_files']}")
        click.echo(f"🏗️ Structure: {analysis['structure']}")
        click.echo(f"🎯 Complexity: {analysis['complexity']}")
        
        if analysis["languages"]:
            click.echo(f"\n🌐 Languages detected:")
            for lang, count in analysis["languages"].items():
                click.echo(f"   📝 {lang}: {count} files")
        
        if analysis["build_systems"]:
            click.echo(f"\n🔧 Build systems:")
            for build_system in analysis["build_systems"]:
                click.echo(f"   ⚙️ {build_system}")
        
        # Save detailed analysis
        analysis_file = repo_path / "repository_analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        click.echo(f"\n📄 Detailed analysis saved to: {analysis_file}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")


# Version Management Commands

@cli.command()
@click.option('--description', '-d', required=True, help='Description of this version')
def create_version(description):
    """Create a manual version snapshot of all documentation."""
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.create_manual_version(description)
        
        if result["success"]:
            click.echo(f"✅ Version created: {result['version_id']}")
            click.echo(f"📝 Description: {description}")
        else:
            click.echo(f"❌ Failed to create version: {result['error']}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
def list_versions():
    """List all available version snapshots."""
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.list_versions()
        
        if result["success"]:
            versions = result["versions"]
            if not versions:
                click.echo("📋 No versions found")
                return
            
            click.echo("📋 Available Versions:")
            click.echo("=" * 80)
            
            for version in versions:
                click.echo(f"🆔 {version['version_id']}")
                click.echo(f"📅 {version['timestamp']}")
                click.echo(f"📝 {version['description']}")
                click.echo(f"🔧 Trigger: {version['trigger']}")
                click.echo(f"📊 Requirements: {version['requirements_count']}, Tests: {version['tests_count']}, Clarifications: {version['clarifications_count']}")
                click.echo("-" * 40)
        else:
            click.echo(f"❌ Failed to list versions: {result['error']}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.argument('version_id')
def restore_version(version_id):
    """Restore a specific version snapshot."""
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.restore_version(version_id)
        
        if result["success"]:
            click.echo(f"✅ Version {version_id} restored successfully")
            click.echo("📁 Files restored:")
            click.echo("   - requirements.gherkin")
            click.echo("   - requirements.md")
            click.echo("   - tests/")
            click.echo("   - traceability_matrix.md")
        else:
            click.echo(f"❌ Failed to restore version {version_id}: {result['error']}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
@click.argument('version1_id')
@click.argument('version2_id')
def compare_versions(version1_id, version2_id):
    """Compare two version snapshots."""
    try:
        workflow = AgentOpsWorkflow()
        result = workflow.compare_versions(version1_id, version2_id)
        
        if result["success"]:
            comparison = result["comparison"]
            click.echo(f"📊 Comparing {version1_id} vs {version2_id}")
            click.echo("=" * 60)
            
            differences = comparison["differences"]
            click.echo(f"📈 Requirements: {differences['requirements_count']:+d}")
            click.echo(f"🧪 Tests: {differences['tests_count']:+d}")
            click.echo(f"💡 Clarifications: {differences['clarifications_count']:+d}")
            
            if differences["new_files"]:
                click.echo(f"📁 New files: {', '.join(differences['new_files'])}")
            if differences["removed_files"]:
                click.echo(f"🗑️ Removed files: {', '.join(differences['removed_files'])}")
        else:
            click.echo(f"❌ Failed to compare versions: {result['error']}")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
def version_info():
    """Show information about the current version system."""
    try:
        workflow = AgentOpsWorkflow()
        versions = workflow.version_manager.list_versions()
        
        click.echo("📋 Version System Information")
        click.echo("=" * 50)
        click.echo(f"📁 Versions directory: {workflow.version_manager.versions_dir}")
        click.echo(f"📊 Total versions: {len(versions)}")
        
        if versions:
            latest = versions[0]  # First in list is most recent
            click.echo(f"🆕 Latest version: {latest.version_id}")
            click.echo(f"📅 Latest timestamp: {latest.timestamp}")
            click.echo(f"📝 Latest description: {latest.description}")
        
        # Check if latest symlink exists
        latest_link = os.path.join(workflow.version_manager.versions_dir, "latest")
        if os.path.exists(latest_link):
            click.echo(f"🔗 Latest symlink: {os.path.realpath(latest_link)}")
        else:
            click.echo("🔗 Latest symlink: Not found")
            
    except Exception as e:
        click.echo(f"❌ Error: {e}")


if __name__ == '__main__':
    cli() 