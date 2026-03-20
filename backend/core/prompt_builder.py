"""
BizPilotAI - Prompt builder utilities.
Constructs structured prompts for different agent types.
"""
from datetime import datetime
from typing import Dict, Any


class PromptBuilder:
    """Builds structured prompts for AI agents."""
    
    @staticmethod
    def build_business_context(business: Dict[str, Any]) -> str:
        """
        Build business context string from business data.
        
        Args:
            business: Business document from MongoDB
            
        Returns:
            Formatted business context string
        """
        context = f"""
Business Name: {business.get('name', 'N/A')}
Industry: {business.get('industry', 'N/A')}
Website: {business.get('website', 'N/A')}
Description: {business.get('description', 'N/A')}
Business Goals: {business.get('goals', 'N/A')}
"""
        return context.strip()
    
    @staticmethod
    def build_marketing_prompt(business: Dict[str, Any]) -> str:
        """Build prompt for marketing agent."""
        context = PromptBuilder.build_business_context(business)
        
        prompt = f"""You are an expert marketing strategist with 15+ years of experience.
Analyze the following business and provide a comprehensive marketing report.

{context}

Please provide a detailed marketing analysis with the following sections:

1. Executive Summary
   - Brief overview of marketing opportunities

2. Industry-Specific Trends
   - Current trends in the {business.get('industry', 'industry')} industry
   - Market dynamics and consumer behavior

3. Target Audience Strategy
   - Identify ideal customer profiles
   - Market segmentation recommendations

4. Brand Positioning
   - Recommended brand positioning strategy
   - Unique value proposition

5. Growth Recommendations
   - Actionable marketing tactics
   - Short-term and long-term strategies
   - Expected impact on business growth

Be specific, data-driven, and provide actionable recommendations.
Format your response in clear sections with headers."""
        
        return prompt
    
    @staticmethod
    def build_finance_prompt(business: Dict[str, Any]) -> str:
        """Build prompt for finance agent."""
        context = PromptBuilder.build_business_context(business)
        
        prompt = f"""You are a financial analyst with 20+ years of experience in business finance.
Analyze the following business and provide a comprehensive financial strategy report.

{context}

Please provide a detailed financial analysis with the following sections:

1. Revenue Model Analysis
   - Assessment of potential revenue streams
   - Pricing strategy recommendations

2. Cost Structure Review
   - Cost reduction opportunities
   - Operational efficiency improvements

3. Profitability Opportunities
   - Margin optimization strategies
   - Ways to increase bottom-line profitability

4. Financial Risks
   - Potential financial challenges
   - Risk mitigation strategies

5. Investment Strategy
   - Recommended investments for growth
   - ROI projections
   - Funding strategy recommendations

Be specific with financial metrics and provide concrete recommendations.
Format your response in clear sections with headers."""
        
        return prompt
    
    @staticmethod
    def build_operations_prompt(business: Dict[str, Any]) -> str:
        """Build prompt for operations agent."""
        context = PromptBuilder.build_business_context(business)
        
        prompt = f"""You are an operations excellence expert with 20+ years of experience.
Analyze the following business and provide a comprehensive operations improvement report.

{context}

Please provide a detailed operations analysis with the following sections:

1. Process Optimization
   - Current process assessment
   - Recommended process improvements
   - Expected efficiency gains

2. Resource Allocation
   - Optimal resource distribution
   - Staffing recommendations
   - Risk mitigation through resource planning

3. Technology Stack Recommendations
   - Recommended tools and technologies
   - Implementation priorities
   - Expected ROI from tech investments

4. Efficiency Improvements
   - Quick wins for immediate impact
   - Long-term efficiency strategies

5. Scaling Plan
   - Roadmap for scaling operations
   - Infrastructure requirements
   - Growth milestones

Provide specific, implementable recommendations.
Format your response in clear sections with headers."""
        
        return prompt
    
    @staticmethod
    def build_sales_prompt(business: Dict[str, Any]) -> str:
        """Build prompt for sales agent."""
        context = PromptBuilder.build_business_context(business)
        
        prompt = f"""You are a sales strategy expert with 15+ years of experience in B2B and B2C sales.
Analyze the following business and provide a comprehensive sales strategy report.

{context}

Please provide a detailed sales analysis with the following sections:

1. Sales Funnel Analysis
   - Current funnel assessment
   - Stage-by-stage optimization opportunities

2. Lead Generation Strategy
   - Recommended lead sources
   - Lead generation tactics
   - Expected lead volume projections

3. Conversion Optimization
   - Sales process optimization
   - Objection handling strategies
   - Close rate improvement tactics

4. Pricing Strategy
   - Competitive pricing analysis
   - Value-based pricing recommendations
   - Price optimization strategies

5. Partnership Opportunities
   - Strategic partnership recommendations
   - Channel expansion strategies
   - Revenue sharing models

Provide specific, actionable sales recommendations.
Format your response in clear sections with headers."""
        
        return prompt
    
    @staticmethod
    def build_strategy_prompt(business: Dict[str, Any]) -> str:
        """Build prompt for strategy agent (CEO-level)."""
        context = PromptBuilder.build_business_context(business)
        
        prompt = f"""You are a strategic business consultant and former C-level executive with 25+ years of experience.
Provide a comprehensive strategic analysis for the following business at CEO level.

{context}

Please provide a detailed strategic analysis with the following sections:

1. Competitive Landscape
   - Market analysis and competitive positioning
   - Key competitors and competitive advantages
   - Market share opportunities

2. SWOT Analysis
   - Strengths: Internal capabilities and advantages
   - Weaknesses: Internal challenges to address
   - Opportunities: External growth opportunities
   - Threats: External risks and challenges

3. Long-Term Roadmap
   - 1-year strategic goals
   - 3-year vision and milestones
   - 5-year transformation strategy

4. Market Expansion Opportunities
   - New market entry strategies
   - Geographic expansion possibilities
   - Product/service line expansion

5. Risk Assessment & Mitigation
   - Critical business risks
   - Risk mitigation strategies
   - Contingency planning recommendations

Provide strategic, high-level recommendations suitable for board presentation.
Format your response in clear sections with headers."""
        
        return prompt
    
    @staticmethod
    def get_prompt_for_agent(agent_name: str, business: Dict[str, Any]) -> str:
        """
        Get the appropriate prompt for an agent.
        
        Args:
            agent_name: Name of the agent
            business: Business document
            
        Returns:
            Formatted prompt string
            
        Raises:
            ValueError: If agent_name is invalid
        """
        agent_name = agent_name.lower().strip()
        
        prompt_builders = {
            "marketing": PromptBuilder.build_marketing_prompt,
            "finance": PromptBuilder.build_finance_prompt,
            "operations": PromptBuilder.build_operations_prompt,
            "sales": PromptBuilder.build_sales_prompt,
            "strategy": PromptBuilder.build_strategy_prompt,
        }
        
        if agent_name not in prompt_builders:
            raise ValueError(
                f"Invalid agent name: {agent_name}. "
                f"Valid agents: {', '.join(prompt_builders.keys())}"
            )
        
        return prompt_builders[agent_name](business)
