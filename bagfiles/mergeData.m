function v2 = mergeData(v1)
    j = 2;
    v2 = zeros(2*length(v1));
    for i = 1:length(v1)
        v2(j) = v1(i);
        v2(j-1) = v1(i);
        j = j + 2;       
    end
end


% function mergeData(t1, v1)
%     j = 1;
%     for i = 1:length(t1)
%         if j == 1 && v1(i) > 0 
%             sprintf('%d: %f', i, v1(i))    
%             sprintf('%d: %f', i, t1(i)/(10^9))    
%             j = 0;
%         end
%         if v1(i) < 0 
%             sprintf('%d: %f', i, v1(i))    
%             sprintf('%d: %f', i, t1(i)/(10^9))    
%             break;    
%         end
%     end
% end

% function mergeData(t1, t2)
%     j = 0;
%     for i = 1:length(t1)
%         if t1(i, 1) >= t2(1, 1)
%             sprintf('%d - %f', i, t1(i,1))    
%             
%             sprintf('%d - %f', i, t2(i,1))
%             break;    
%         end
%     end
% end


% function mergeData(t1, t2)
%     for i = 1:length(t1)
%         for j = 1: length(t2)
%             if t1(i, 1) == t1(j, 1)
%                 sprintf('%f %d', t2(j,1))    
%                 sprintf('%f %d', t2(j,1))    
%             end
%         end
%                
%     end
% end
