

class GuardrailsResponse(dict):
    """
    A wrapper class for Enkrypt AI API responses that provides additional functionality
    while maintaining backward compatibility with dictionary access.
    """
    
    def __init__(self, response_data: dict):
        """
        Initialize the Response object with API response data.
        
        Args:
            response_data (dict): The raw API response dictionary
        """
        super().__init__(response_data)
        self._data = response_data

    def get_summary(self) -> dict:
        """
        Get the summary section of the response.
        
        Returns:
            dict: The summary data or empty dict if not found
        """
        return self._data.get("summary", {})

    def get_details(self) -> dict:
        """
        Get the details section of the response.
        
        Returns:
            dict: The details data or empty dict if not found
        """
        return self._data.get("details", {})

    def has_violations(self) -> bool:
        """
        Check if any detectors found violations in the content.
        
        Returns:
            bool: True if any detector reported a violation (score > 0), False otherwise
        """
        summary = self.get_summary()
        for key, value in summary.items():
            if key == "toxicity" and isinstance(value, list) and len(value) > 0:
                return True
            elif isinstance(value, (int, float)) and value > 0:
                return True
        return False

    def get_violations(self) -> list[str]:
        """
        Get a list of detector names that found violations.
        
        Returns:
            list[str]: Names of detectors that reported violations
        """
        summary = self.get_summary()
        violations = []
        for detector, value in summary.items():
            if detector == "toxicity" and isinstance(value, list) and len(value) > 0:
                violations.append(detector)
            elif isinstance(value, (int, float)) and value > 0:
                violations.append(detector)
        return violations

    def is_safe(self) -> bool:
        """
        Check if the content is safe (no violations detected).
        
        Returns:
            bool: True if no violations were detected, False otherwise
        """
        return not self.has_violations()
    
    def is_attack(self) -> bool:
        """
        Check if the content is attacked (violations detected).
        
        Returns:
            bool: True if violations were detected, False otherwise
        """
        return self.has_violations()

    def __str__(self) -> str:
        """
        String representation of the response.
        
        Returns:
            str: A formatted string showing summary and violation status
        """
        violations = self.get_violations()
        status = "UNSAFE" if violations else "SAFE"
        
        if violations:
            violation_str = f"Violations detected: {', '.join(violations)}"
        else:
            violation_str = "No violations detected"
            
        return f"Response Status: {status}\n{violation_str}"
    
    
class PIIResponse(dict):
    """
    A wrapper class for Enkrypt AI PII API responses that provides additional functionality
    while maintaining backward compatibility with dictionary access.
    """ 
    
    def __init__(self, response_data: dict):
        """
        Initialize the Response object with API response data.
        
        Args:
            response_data (dict): The raw API response dictionary
        """ 
        super().__init__(response_data)
        self._data = response_data

    def get_text(self) -> str:
        """
        Get the text section of the response.
        
        Returns:
            str: The text data or empty string if not found
        """ 
        return self._data.get("text", "")

    def get_key(self) -> str:
        """
        Get the key section of the response.
        """ 
        return self._data.get("key", "")
    
    