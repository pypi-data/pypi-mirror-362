import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class StepType(Enum):
    GIVEN = "Given"
    WHEN = "When"
    THEN = "Then"
    AND = "And"
    BUT = "But"

@dataclass
class Step:
    """Represents a single Gherkin step"""
    type: StepType
    text: str
    line_number: int
    parsed_inputs: Dict[str, str] = None
    
    def __post_init__(self):
        if self.parsed_inputs is None:
            self.parsed_inputs = {}
        self._parse_inputs()
    
    def _parse_inputs(self):
        """Parse inputs with double backticks or brackets as recommended in the guide"""
        # Pattern for username="value" or username=[value]
        input_pattern = r'(\w+)=(?:"([^"]+)"|(\[([^\]]+)\]))'
        matches = re.findall(input_pattern, self.text)
        
        for match in matches:
            key = match[0]
            value = match[1] if match[1] else match[3]  # quoted or bracketed value
            self.parsed_inputs[key] = value
        
        # Pattern for quoted strings that might be page names, button names, etc.
        quoted_pattern = r'"([^"]+)"'
        quoted_matches = re.findall(quoted_pattern, self.text)
        
        # Store quoted elements for easy access
        if quoted_matches:
            self.parsed_inputs['quoted_elements'] = quoted_matches

@dataclass
class Scenario:
    """Represents a Gherkin scenario"""
    name: str
    steps: List[Step]
    line_number: int
    is_outline: bool = False
    examples: List[Dict[str, str]] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.examples is None:
            self.examples = []
        if self.tags is None:
            self.tags = []
    
    def validate_aaa_pattern(self) -> Dict[str, bool]:
        """Validate if scenario follows AAA (Arrange-Act-Assert) pattern"""
        has_given = any(step.type == StepType.GIVEN for step in self.steps)
        has_when = any(step.type == StepType.WHEN for step in self.steps)
        has_then = any(step.type == StepType.THEN for step in self.steps)
        
        return {
            'has_arrange': has_given,
            'has_act': has_when,
            'has_assert': has_then,
            'follows_aaa': has_given and has_when and has_then
        }

@dataclass
class Background:
    """Represents Gherkin background steps"""
    steps: List[Step]
    line_number: int

@dataclass
class Feature:
    """Represents a complete Gherkin feature"""
    name: str
    description: str
    scenarios: List[Scenario]
    background: Optional[Background] = None
    tags: List[str] = None
    line_number: int = 1
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class GherkinParser:
    """Optimized Gherkin parser following Hercules best practices"""
    
    def __init__(self):
        self.step_keywords = {
            'Given': StepType.GIVEN,
            'When': StepType.WHEN,
            'Then': StepType.THEN,
            'And': StepType.AND,
            'But': StepType.BUT
        }
        
        # Compile regex patterns for better performance
        self.feature_pattern = re.compile(r'^Feature:\s*(.+)$', re.IGNORECASE)
        self.scenario_pattern = re.compile(r'^Scenario(?:\s+Outline)?:\s*(.+)$', re.IGNORECASE)
        self.background_pattern = re.compile(r'^Background:\s*$', re.IGNORECASE)
        self.step_pattern = re.compile(r'^(Given|When|Then|And|But)\s+(.+)$', re.IGNORECASE)
        self.tag_pattern = re.compile(r'^@(\w+)(?:\s+@(\w+))*')
        self.examples_pattern = re.compile(r'^Examples:\s*$', re.IGNORECASE)
        self.table_pattern = re.compile(r'^\s*\|(.+)\|\s*$')
    
    def parse(self, gherkin_text: str) -> Feature:
        """Parse Gherkin text and return Feature object"""
        lines = gherkin_text.strip().split('\n')
        return self._parse_lines(lines)
    
    def parse_file(self, file_path: str) -> Feature:
        """Parse Gherkin file and return Feature object"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse(content)
    
    def _parse_lines(self, lines: List[str]) -> Feature:
        """Internal method to parse lines into Feature object"""
        feature = None
        current_scenario = None
        current_background = None
        current_tags = []
        current_step_type = None
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                i += 1
                continue
            
            # Parse tags
            if line.startswith('@'):
                current_tags.extend(self._parse_tags(line))
                i += 1
                continue
            
            # Parse feature
            feature_match = self.feature_pattern.match(line)
            if feature_match:
                feature_name = feature_match.group(1)
                feature_description = self._parse_description(lines, i + 1)
                feature = Feature(
                    name=feature_name,
                    description=feature_description,
                    scenarios=[],
                    tags=current_tags.copy(),
                    line_number=i + 1
                )
                current_tags.clear()
                i += 1
                continue
            
            # Parse background
            if self.background_pattern.match(line):
                current_background = Background(steps=[], line_number=i + 1)
                i += 1
                continue
            
            # Parse scenario
            scenario_match = self.scenario_pattern.match(line)
            if scenario_match:
                if current_scenario and feature:
                    feature.scenarios.append(current_scenario)
                
                scenario_name = scenario_match.group(1)
                is_outline = 'outline' in line.lower()
                
                current_scenario = Scenario(
                    name=scenario_name,
                    steps=[],
                    line_number=i + 1,
                    is_outline=is_outline,
                    tags=current_tags.copy()
                )
                current_tags.clear()
                current_step_type = None
                i += 1
                continue
            
            # Parse examples
            if self.examples_pattern.match(line) and current_scenario:
                examples_data = self._parse_examples(lines, i + 1)
                current_scenario.examples = examples_data['examples']
                i = examples_data['next_line']
                continue
            
            # Parse steps
            step_match = self.step_pattern.match(line)
            if step_match:
                step_keyword = step_match.group(1)
                step_text = step_match.group(2)
                
                # Handle And/But by using the previous step type
                if step_keyword.lower() in ['and', 'but']:
                    if current_step_type:
                        step_type = current_step_type
                    else:
                        step_type = self.step_keywords.get(step_keyword, StepType.GIVEN)
                else:
                    step_type = self.step_keywords.get(step_keyword, StepType.GIVEN)
                    current_step_type = step_type
                
                step = Step(
                    type=step_type,
                    text=step_text,
                    line_number=i + 1
                )
                
                # Add to current scenario or background
                if current_scenario:
                    current_scenario.steps.append(step)
                elif current_background:
                    current_background.steps.append(step)
                
                i += 1
                continue
            
            i += 1
        
        # Add the last scenario if exists
        if current_scenario and feature:
            feature.scenarios.append(current_scenario)
        
        # Add background if exists
        if current_background and feature:
            feature.background = current_background
        
        if not feature:
            raise ValueError("No feature found in the provided Gherkin text")
        
        return feature
    
    def _parse_tags(self, line: str) -> List[str]:
        """Parse tags from a line"""
        tags = []
        for tag in line.split():
            if tag.startswith('@'):
                tags.append(tag[1:])  # Remove @ symbol
        return tags
    
    def _parse_description(self, lines: List[str], start_index: int) -> str:
        """Parse feature description"""
        description_lines = []
        i = start_index
        
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith('#'):
                i += 1
                continue
            
            # Stop at first keyword
            if (self.scenario_pattern.match(line) or 
                self.background_pattern.match(line) or 
                line.startswith('@')):
                break
            
            description_lines.append(line)
            i += 1
        
        return '\n'.join(description_lines)
    
    def _parse_examples(self, lines: List[str], start_index: int) -> Dict:
        """Parse examples table for scenario outline"""
        examples = []
        headers = []
        i = start_index
        
        while i < len(lines):
            line = lines[i].strip()
            
            if not line or line.startswith('#'):
                i += 1
                continue
            
            table_match = self.table_pattern.match(line)
            if table_match:
                row_data = [cell.strip() for cell in table_match.group(1).split('|')]
                
                if not headers:
                    headers = row_data
                else:
                    if len(row_data) == len(headers):
                        examples.append(dict(zip(headers, row_data)))
                i += 1
                continue
            
            # Stop at non-table content
            break
        
        return {'examples': examples, 'next_line': i}
    
    def validate_hercules_best_practices(self, feature: Feature) -> Dict[str, List[str]]:
        """Validate feature against Hercules best practices"""
        issues = []
        recommendations = []
        
        for scenario in feature.scenarios:
            # Check AAA pattern
            aaa_validation = scenario.validate_aaa_pattern()
            if not aaa_validation['follows_aaa']:
                issues.append(f"Scenario '{scenario.name}' doesn't follow AAA pattern")
            
            # Check for single responsibility
            then_count = sum(1 for step in scenario.steps if step.type == StepType.THEN)
            if then_count > 1:
                recommendations.append(f"Scenario '{scenario.name}' has multiple assertions, consider splitting")
            
            # Check for descriptive naming
            for step in scenario.steps:
                if 'that button' in step.text.lower() or 'the field' in step.text.lower():
                    issues.append(f"Step '{step.text}' uses generic references")
                
                # Check for proper input formatting
                if '=' in step.text and not step.parsed_inputs:
                    recommendations.append(f"Step '{step.text}' could use better input formatting")
        
        return {
            'issues': issues,
            'recommendations': recommendations
        }

# Example usage and utility functions
def format_feature_summary(feature: Feature) -> str:
    """Generate a formatted summary of the parsed feature"""
    summary = f"Feature: {feature.name}\n"
    summary += f"Description: {feature.description}\n"
    summary += f"Tags: {', '.join(feature.tags) if feature.tags else 'None'}\n"
    
    if feature.background:
        summary += f"\nBackground Steps: {len(feature.background.steps)}\n"
    
    summary += f"\nScenarios: {len(feature.scenarios)}\n"
    
    for i, scenario in enumerate(feature.scenarios, 1):
        summary += f"  {i}. {scenario.name}"
        if scenario.is_outline:
            summary += f" (Outline with {len(scenario.examples)} examples)"
        summary += f" - {len(scenario.steps)} steps\n"
    
    return summary

# Example Gherkin text
sample_gherkin = """
    @smoke @regression
    Feature: User Account Registration
    As a new user
    I want to register for an account
    So that I can access the platform
    
    Background:
        Given I have accessed the "Registration Page"
        And the registration form is displayed
    
    @happy-path
    Scenario: Successful user registration
        Given I am on the registration page
        When I enter username="john_doe" and password="SecurePass123"
        And I click the "Submit" button
        Then I should see "Registration successful" message
        And I should be redirected to the "Welcome" page
    
    @data-driven
    Scenario Outline: Registration with different user types
        Given I am on the registration page
        When I enter username="<username>" and user_type="<type>"
        And I submit the registration form
        Then I should see "<expected_message>"
        
        Examples:
            | username | type    | expected_message |
            | admin    | admin   | Admin registered |
            | user     | regular | User registered  |
    """